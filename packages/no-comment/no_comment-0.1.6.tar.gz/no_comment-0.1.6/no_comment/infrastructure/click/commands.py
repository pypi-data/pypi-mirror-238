# No Comment --- Comment any resource on the web!
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime as DateTime
from datetime import timezone
from pathlib import Path
from typing import Any, Iterator
from uuid import uuid4

from no_comment.domain.commenting.entities import Comment
from no_comment.domain.commenting.repositories import Comments, Streams
from no_comment.domain.commenting.value_objects import (
    CommentId,
    DateAndTime,
    StreamId,
    Text,
    Url,
)

NOW = DateTime.now(timezone.utc)


@dataclass
class Data:
    url: str
    title: str
    rating: str
    text: str
    created: DateTime
    tags: list[str] = field(default_factory=list)


def convert(data_file: Path, created_file: Path) -> None:
    created = load_created(created_file)

    for c in extract_data(data_file):
        comment = {
            "id": str(uuid4()),
            "url": c.url,
            "created": created.get(c.url, NOW).strftime("%Y-%m-%d %H:%M:%S"),
            "text": extract_text(c),
            "tags": c.tags,
            "rating": c.rating,
        }
        print(json.dumps(comment))


def load_created(path: Path) -> dict[str, DateTime]:
    result: dict[str, DateTime] = {}
    for line in path.read_text().splitlines():
        d, t, u = line.split(" ", 3)
        result[u] = DateTime.strptime(f"{d} {t}", "%Y-%m-%d %H:%M:%S+00:00")
    return result


def extract_text(data: Data) -> str:
    text = data.title.strip("\n")
    if text:
        text = text + "\n\n"
    if data.text:
        text += data.text.strip("\n")

    tags = []
    for e in data.tags:
        if e not in text:
            tags.append(e)
        else:
            text = text.replace(e, f"#{e}")

    if tags:
        text = text.rstrip("\n") + "\n\n" + " ".join([f"#{t}" for t in tags])

    return text.strip()


def extract_data(path: Path) -> Iterator[Data]:
    data = Data("", "", "", "", NOW)
    motif_etiquette = re.compile(r"^  \* ([^\n|:]*):(.*)")

    for line in path.read_text().splitlines():
        if line.startswith("- http"):
            if data.url:
                yield data

            url = line[1:].strip()
            data = Data(url, "", "", "", NOW)
            continue

        if res := motif_etiquette.search(line):
            att = res.group(1)
            val = res.group(2).strip()
            if att == "tag":
                data.tags.append(val)
            elif att == "tags":
                data.tags.extend([t.strip() for t in val.split(",")])
            elif att == "title":
                data.title = val
            elif att == "rating":
                data.rating = val
            else:
                # Some texts contain « : »
                data.text = att + ":" + val
        elif line.startswith("  * "):
            data.text = line.strip()[2:]
        elif line.startswith("    "):
            data.text += "\n" + line.strip()

    # Last line
    if data.url:
        yield data


def dispatch_comments(comments: Path, categories: list[str]) -> None:
    processed_urls = find_processed_urls(categories)

    choices = ", ".join([f"{idx + 1}) {name}" for idx, name in enumerate(categories)])
    question = f"Dispatch to {choices}"

    files: dict[str, Any] = {}
    for c in categories:
        files[c] = category_path(c).open("a")

    resuming = True
    for line in comments.read_text().splitlines():
        comment = json.loads(line.strip())
        if resuming and comment["url"] in processed_urls:
            print(f"SKIPPING: {comment['url']}")
            continue
        if resuming:
            resuming = False
        else:
            os.system("clear")
        print(f"<{comment['url']}>")
        print(comment["created"])
        print(comment["text"])
        print()
        print(question)
        choice = input("Choice? ")
        category = categories[int(choice) - 1]
        fh = files[category]
        fh.write(f"{line}\n")

    for fh in files.values():
        fh.close()


def find_processed_urls(categories: list[str]) -> list[str]:
    result: list[str] = []
    for c in categories:
        for line in category_path(c).read_text().splitlines():
            result.append(json.loads(line)["url"])
    return result


def category_path(category: str) -> Path:
    return Path(f"comments-{category}.jsons")


def import_to(streams: Streams, stream_id: str, comments: Comments) -> None:
    stream = streams.by_id(StreamId(stream_id))
    if not stream:
        print(f"Stream `{stream_id}` does not exist!")
        sys.exit(2)

    for line in sys.stdin:
        data = json.loads(line.strip())

        comment = Comment(
            CommentId.instanciate(data["id"]),
            Url.instanciate(data["url"]),
            Text.instanciate(data["text"]),
            DateAndTime.from_isoformat(data["created_at"]),
        )
        comments.add(stream.id, comment)
    return


def export_from(streams: Streams, stream_id: str, comments: Comments) -> None:
    stream = streams.by_id(StreamId(stream_id))
    if not stream:
        print(f"Stream `{stream_id}` does not exist!")
        sys.exit(2)

    for comment in comments.on_stream(stream.id):
        print(
            json.dumps(
                {
                    "id": str(comment.id),
                    "url": str(comment.url),
                    "text": str(comment.text),
                    "created_at": comment.created_at.to_isoformat(),
                }
            )
        )
