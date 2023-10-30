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
from uuid import uuid4

from no_comment.domain.commenting.entities import Comment
from no_comment.domain.commenting.exceptions import InvalidValue
from no_comment.domain.commenting.repositories import Comments
from no_comment.domain.commenting.services import Calendar
from no_comment.domain.commenting.value_objects import CommentId, StreamId, Text, Url


@dataclass
class Request:
    stream_id: str
    url: str
    text: str


class Presenter(ABC):
    @abstractmethod
    def bad_parameter(self, name: str, value: str) -> None:
        ...

    @abstractmethod
    def comment_added(self, comment: Comment) -> None:
        ...


@dataclass
class Interactor:
    presenter: Presenter
    comments: Comments
    calendar: Calendar

    def execute(self, request: Request) -> None:
        try:
            url = Url.instanciate(request.url)
        except InvalidValue:
            return self.presenter.bad_parameter("url", "")

        try:
            text = Text.instanciate(request.text)
        except InvalidValue:
            return self.presenter.bad_parameter("text", "")

        # Comment should be built by a comment factory
        comment_id = CommentId.instanciate(str(uuid4()))
        stream_id = StreamId(request.stream_id)
        comment = Comment(comment_id, url, text, self.calendar.now())

        self.comments.add(stream_id, comment)
        self.presenter.comment_added(comment)
