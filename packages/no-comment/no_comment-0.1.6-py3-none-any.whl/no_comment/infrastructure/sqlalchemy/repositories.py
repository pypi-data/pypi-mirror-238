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

from datetime import timezone
from typing import Any, Optional

from sqlalchemy import Column, DateTime, MetaData, String, Table, insert, select
from sqlalchemy.engine import Connection

from no_comment.domain.commenting.entities import Comment, Stream
from no_comment.domain.commenting.repositories import Comments as CommentsInterface
from no_comment.domain.commenting.repositories import Streams as StreamsInterface
from no_comment.domain.commenting.value_objects import (
    Author,
    CommentId,
    DateAndTime,
    Description,
    StreamId,
    Text,
    Title,
    Url,
)

META_DATA = MetaData()
DEFAULT_PAGE_SIZE = 10


streams = Table(
    "streams",
    META_DATA,
    Column("id", String(StreamId.MAX), primary_key=True),
    Column("title", String(Title.MAX), nullable=False),
    Column("description", String(Description.MAX), nullable=False),
    Column("author", String(Author.MAX), nullable=False),
    Column("created_at", DateTime(), nullable=False),
)


class Streams(StreamsInterface):
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def by_id(self, stream_id: StreamId) -> Optional[Stream]:
        stmt = select(streams).where(streams.c.id == str(stream_id))
        if row := self.__connection.execute(stmt).first():  # type: ignore[var-annotated]
            return self.__row_to_stream(row)
        return None

    def __row_to_stream(self, row: Any) -> Stream:
        return Stream(
            StreamId(row.id),
            Title(row.title),
            Description(row.description),
            Author(row.author),
            DateAndTime(row.created_at.replace(tzinfo=timezone.utc)),
        )

    def all(self) -> list[Stream]:
        stmt = select(streams)
        return [
            self.__row_to_stream(row)
            for row in self.__connection.execute(stmt).fetchall()
        ]

    def add(self, stream: Stream) -> None:
        stmt = insert(streams).values(
            id=str(stream.id),
            title=str(stream.title),
            description=str(stream.description),
            author=str(stream.author),
            created_at=stream.created_at.to_datetime(),
        )
        self.__connection.execute(stmt)


comments = Table(
    "comments",
    META_DATA,
    Column("id", String(CommentId.MAX), primary_key=True),
    Column("stream_id", String(StreamId.MAX), nullable=False),
    Column("url", String(Url.MAX), nullable=False),
    Column("text", String(Text.MAX), nullable=False),
    Column("created_at", DateTime(), nullable=False),
)


class Comments(CommentsInterface):
    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def on_stream(
        self,
        stream_id: StreamId,
        /,
        *,
        latest_first: bool = True,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        url: Optional[Url] = None,
    ) -> list[Comment]:
        stmt = select(comments).where(comments.c.stream_id == str(stream_id))

        if url:
            stmt = stmt.where(comments.c.url == str(url))  # type: ignore[attr-defined]

        if page:
            size = page_size or DEFAULT_PAGE_SIZE
            stmt = stmt.offset((page - 1) * size)  # type: ignore[attr-defined]
            stmt = stmt.limit(size)  # type: ignore[attr-defined]

        stmt = stmt.order_by(comments.c.created_at.desc())  # type: ignore[attr-defined]

        return [  # type: ignore[var-annotated]
            self.__row_to_comment(row) for row in self.__connection.execute(stmt)
        ]

    def __row_to_comment(self, row: Any) -> Comment:
        return Comment(
            CommentId(row.id),
            Url(row.url),
            Text(row.text),
            DateAndTime(row.created_at.replace(tzinfo=timezone.utc)),
        )

    def add(self, stream_id: StreamId, comment: Comment) -> None:
        stmt = insert(comments).values(
            id=str(comment.id),
            stream_id=str(stream_id),
            url=str(comment.url),
            text=str(comment.text),
            created_at=comment.created_at.to_datetime(),
        )
        self.__connection.execute(stmt)
