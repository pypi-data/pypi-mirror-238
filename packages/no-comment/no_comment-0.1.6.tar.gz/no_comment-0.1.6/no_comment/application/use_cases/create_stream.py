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

from no_comment.domain.commenting.entities import Stream
from no_comment.domain.commenting.exceptions import InvalidValue
from no_comment.domain.commenting.repositories import Streams
from no_comment.domain.commenting.services import Calendar
from no_comment.domain.commenting.value_objects import (
    Author,
    Description,
    StreamId,
    Title,
)


@dataclass
class Request:
    stream_id: str
    title: str
    description: str
    author: str


class Presenter(ABC):
    @abstractmethod
    def bad_parameter(self, message: str) -> None:
        ...

    @abstractmethod
    def stream_already_exists(self, stream: Stream) -> None:
        ...

    @abstractmethod
    def stream_created(self, stream: Stream) -> None:
        ...


@dataclass
class Interactor:
    presenter: Presenter
    streams: Streams
    calendar: Calendar

    def execute(self, request: Request) -> None:
        try:
            stream_id = StreamId.instanciate(request.stream_id)
            title = Title.instanciate(request.title)
            description = Description.instanciate(request.description)
            author = Author.instanciate(request.author)
        except InvalidValue as exc:
            return self.presenter.bad_parameter(str(exc))

        if stream := self.streams.by_id(stream_id):
            return self.presenter.stream_already_exists(stream)

        stream = Stream(stream_id, title, description, author, self.calendar.now())

        self.streams.add(stream)
        self.presenter.stream_created(stream)
