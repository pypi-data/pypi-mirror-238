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
from typing import Optional

from .entities import Comment, Stream
from .value_objects import StreamId, Url


class Streams(ABC):
    @abstractmethod
    def by_id(self, stream_id: StreamId) -> Optional[Stream]:
        ...

    @abstractmethod
    def add(self, stream: Stream) -> None:
        ...

    @abstractmethod
    def all(self) -> list[Stream]:
        ...


class Comments(ABC):
    @abstractmethod
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
        ...

    @abstractmethod
    def add(self, stream_id: StreamId, comment: Comment) -> None:
        ...
