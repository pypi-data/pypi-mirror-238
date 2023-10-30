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

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from no_comment.domain.commenting.services import Calendar
from no_comment.infrastructure.settings import CliSettings
from no_comment.infrastructure.sqlalchemy.repositories import Comments, Streams


@contextmanager
def get_connection(settings: CliSettings) -> Iterator[Connection]:
    engine = create_engine(settings.DSN)
    connection = engine.connect()
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def get_calendar() -> Calendar:
    return Calendar()


def get_comments(connection: Connection) -> Comments:
    return Comments(connection)


def get_streams(connection: Connection) -> Streams:
    return Streams(connection)
