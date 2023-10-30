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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from no_comment.domain.commenting.entities import Comment, Stream
from no_comment.domain.commenting.exceptions import InvalidValue
from no_comment.domain.commenting.repositories import Comments, Streams
from no_comment.domain.commenting.value_objects import StreamId, Url


@dataclass
class Request:
    stream_id: str
    url: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class Presenter(ABC):
    @abstractmethod
    def bad_request(self) -> None:
        ...

    @abstractmethod
    def unknown_stream(self, stream_id: StreamId) -> None:
        ...

    @abstractmethod
    def stream(self, stream: Stream) -> None:
        ...

    @abstractmethod
    def comment(self, comment: Comment) -> None:
        ...


@dataclass
class Interactor:
    presenter: Presenter
    streams: Streams
    comments: Comments

    def execute(self, request: Request) -> None:
        try:
            stream_id = StreamId.instanciate(request.stream_id)
        except InvalidValue:
            return self.presenter.bad_request()

        if not (stream := self.streams.by_id(stream_id)):
            return self.presenter.unknown_stream(stream_id)

        self.presenter.stream(stream)

        for comment in self.comments.on_stream(
            stream.id,
            url=Url(request.url) if request.url else None,
            page=request.page,
            page_size=request.page_size,
            latest_first=True,
        ):
            self.presenter.comment(comment)
