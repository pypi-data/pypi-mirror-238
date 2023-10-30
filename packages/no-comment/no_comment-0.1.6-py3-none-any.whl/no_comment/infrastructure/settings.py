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
from typing import Optional

import bl_seth


@dataclass(frozen=True)
class TotpSettings(bl_seth.Settings):
    SECRET: str
    """The secret key.
    It can be generated with `pyotp.random_base32()`."""


@dataclass(frozen=True)
class CliSettings(bl_seth.Settings):
    DSN: str
    """The data source name to access the database.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    TIMEZONE: str = "Europe/Paris"
    """The timezone used to format date & time."""


@dataclass(frozen=True)
class WsgiSettings(bl_seth.Settings):
    SECRET_KEY: str
    """The secret key for Flask sessions.
    See: <https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions>."""

    DSN: str
    """The data source name to access the database.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls>."""

    TIMEZONE: str = "Europe/Paris"
    """The timezone used to format date & time."""

    PROXIED: bool = False
    """To let Flask know that it runs behind a proxy.
    See: <https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/>."""

    DEBUG_SQL: bool = False
    """To enable SqlAlchemy logging.
    See: <https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging>."""

    AUTHORIZED_IP: str = ""
    """The trusted IP address for which the user is automatically authentified.
    A subnetwork can be authorized using a single `*`, for instance `192.168.0.*`."""

    TOTP: Optional[TotpSettings] = None
    """To configure time-based one-time password.
    Extra dependencies must be installed: `no-comment[totp]`."""
