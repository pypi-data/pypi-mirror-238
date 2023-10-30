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

from typing import Any, Optional

from flask import g, session
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from no_comment.domain.commenting.services import Calendar
from no_comment.infrastructure.settings import WsgiSettings
from no_comment.infrastructure.sqlalchemy.repositories import Comments, Streams
from no_comment.interfaces import User

__SETTINGS: Optional[WsgiSettings] = None


def define_settings(settings: WsgiSettings) -> None:
    global __SETTINGS
    __SETTINGS = settings


def get_settings() -> WsgiSettings:
    if not __SETTINGS:
        raise RuntimeError("You must define the settings!")
    return __SETTINGS


def get_connection() -> Connection:
    s = get_settings()
    if "connection" not in g:
        options: dict[str, Any] = {}
        if s.DEBUG_SQL:
            options["echo"] = True
            options["echo_pool"] = "debug"

        engine = create_engine(s.DSN, **options)
        g.setdefault("connection", engine.connect())

    return g.connection  # type: ignore[no-any-return]


def teardown_connection(exception: Optional[BaseException]) -> None:
    if connection := g.pop("connection", None):
        if exception:
            connection.rollback()
        else:
            connection.commit()
        connection.close()


def get_streams() -> Streams:
    return Streams(get_connection())


def get_comments() -> Comments:
    return Comments(get_connection())


def get_calendar() -> Calendar:
    return Calendar()


def get_user() -> User:
    if "user" not in g:
        if user_id := session.get("user_id", ""):
            g.setdefault("user", User(user_id))
        else:
            g.setdefault("user", None)

    return g.user  # type: ignore[no-any-return]
