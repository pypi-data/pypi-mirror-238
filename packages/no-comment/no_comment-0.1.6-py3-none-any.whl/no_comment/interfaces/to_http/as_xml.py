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

from datetime import datetime, timezone
from email.utils import format_datetime
from http import HTTPStatus as HTTP

from no_comment.application.use_cases import display_stream
from no_comment.domain.commenting import entities, value_objects
from no_comment.interfaces.to_http import HttpPresenter


class XmlPresenter(HttpPresenter):
    def __init__(self, content_type: str = "application/xml") -> None:
        self.__status_code: HTTP = HTTP.OK
        self.__headers: dict[str, str] = {"Content-Type": content_type}
        self.__data: str = ""

    def status_code(self) -> int:
        return int(self.__status_code)

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.__data


class DisplayStreamAsAtom(display_stream.Presenter, XmlPresenter):
    def __init__(self, url_self: str, url_alternate: str) -> None:
        super().__init__("application/atom+xml;charset=utf-8")
        self.__url_self = url_self
        self.__url_alternate = url_alternate
        self.__error = ""
        self.__entries = ""
        self.__updated_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.__id = ""
        self.__title = ""
        self.__description = ""
        self.__author = ""

    def data(self) -> str:
        if self.__error:
            return ""

        return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>{self.__id}</id>
    <title>{self.__title}</title>
    <link rel="self" type="application/atom+xml" href="{self.__url_self}" />
    <link rel="alternate" type="text/html" href="{self.__url_alternate}" />
    <updated>{format_datetime(self.__updated_at)}</updated>
    <author>
        <name>{self.__author}</name>
    </author>
    <link href="http://creativecommons.org/licenses/by-sa/1.0/legalcode" rel="license" />
    {self.__entries}
</feed>"""

    def bad_request(self) -> None:
        self.__error = "bad request"
        self.set_status_code(HTTP.BAD_REQUEST)

    def unknown_stream(self, stream_id: value_objects.StreamId) -> None:
        self.__error = "unknown stream"
        self.set_status_code(HTTP.NOT_FOUND)

    def stream(self, stream: entities.Stream) -> None:
        self.__title = str(stream.title)
        self.__description = str(stream.description)
        self.__author = str(stream.author)

    def comment(self, comment: entities.Comment) -> None:
        updated_at = comment.created_at.to_datetime()
        if updated_at > self.__updated_at:
            self.__updated_at = updated_at
        self.__entries += f"""
    <entry>
        <id>urn:uuid:{comment.id}</id>
        <title>{comment_title(comment)}</title>
        <link rel="via" href="{comment.url}" />
        <updated>{format_datetime(updated_at)}</updated>
        <content>{comment.text}</content>
    </entry>"""


class DisplayStreamAsRss(display_stream.Presenter, XmlPresenter):
    def __init__(self, url_self: str, url_alternate: str) -> None:
        super().__init__("application/rss+xml;charset=utf-8")
        self.__url_self = url_self
        self.__url_alternate = url_alternate
        self.__error = ""
        self.__items = ""
        self.__updated_at = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.__title = ""
        self.__description = ""
        self.__author = ""

    def data(self) -> str:
        if self.__error:
            return ""

        return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{self.__title}</title>
        <description>{self.__description}</description>
        <lastBuildDate>{format_datetime(self.__updated_at)}</lastBuildDate>
        <link>{self.__url_alternate}</link>
        <atom:link href="{self.__url_self}.rss" rel="self" type="application/rss+xml" />
        {self.__items}
    </channel>
</rss>"""

    def bad_request(self) -> None:
        self.__error = "bad request"
        self.set_status_code(HTTP.BAD_REQUEST)

    def unknown_stream(self, stream_id: value_objects.StreamId) -> None:
        self.__error = "unknown stream"
        self.set_status_code(HTTP.NOT_FOUND)

    def stream(self, stream: entities.Stream) -> None:
        self.__title = str(stream.title)
        self.__description = str(stream.description)
        self.__author = str(stream.author)

    def comment(self, comment: entities.Comment) -> None:
        updated_at = comment.created_at.to_datetime()
        if updated_at > self.__updated_at:
            self.__updated_at = updated_at
        self.__items += f"""
        <item>
            <title>{comment_title(comment)}</title>
            <link>{comment.url}</link>
            <description>{comment.text}</description>
            <pubDate>{format_datetime(updated_at)}</pubDate>
            <guid isPermaLink="false">urn:uuid:{comment.id}</guid>
        </item>"""


def comment_title(comment: entities.Comment) -> str:
    TITLE_MAX_LENGTH = 30

    title = str(comment.text).split("\n")[0]
    if len(title) > TITLE_MAX_LENGTH:
        return title[0 : TITLE_MAX_LENGTH - 1] + "…"
    return title
