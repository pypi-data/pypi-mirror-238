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

from urllib.parse import urlparse

import bl3d

from no_comment.domain.commenting.exceptions import InvalidUrl

DateAndTime = bl3d.DateAndTime
String = bl3d.String


class StreamId(String):
    MIN: int = 1
    MAX: int = 42


class UniversalUniqueIdentifier(String):
    MIN: int = 36
    MAX: int = 36


class CommentId(UniversalUniqueIdentifier):
    pass


class Text(String):
    MIN = 1
    MAX = 2000


class Url(String):
    MIN = 1
    # Source: <https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers>.  # noqa
    MAX = 2000

    @classmethod
    def instanciate(cls, value: str) -> "Url":
        _ = String.instanciate(value)

        url = urlparse(value)
        if not url.scheme or not url.netloc:
            raise InvalidUrl(value)

        return cls(value)


class Title(String):
    MIN = 1
    MAX = 100


class Description(String):
    MIN = 0
    MAX = 500


class Author(String):
    MIN = 1
    MAX = 100
