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

from dataclasses import dataclass

from .value_objects import (
    Author,
    CommentId,
    DateAndTime,
    Description,
    StreamId,
    Text,
    Title,
    Url,
)


@dataclass
class Stream:
    id: StreamId
    title: Title
    description: Description
    author: Author
    created_at: DateAndTime


@dataclass
class Comment:
    id: CommentId
    url: Url
    text: Text
    created_at: DateAndTime
