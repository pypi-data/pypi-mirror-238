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

from datetime import timedelta

from flask import Flask, get_flashed_messages, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import no_comment.interfaces.to_http.as_html as html_presenters
from no_comment import __version__
from no_comment.infrastructure.settings import WsgiSettings

from . import services
from .auth import blueprint as auth
from .streams import blueprint as streams


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    app = Flask(
        __name__,
        static_url_path="/resources",
        static_folder="./static/",
    )

    configure(app, settings)
    register_blueprints(app, settings)
    register_globals(settings)

    app.teardown_appcontext(services.teardown_connection)

    return app


def configure(app: Flask, settings: WsgiSettings) -> None:
    if settings.PROXIED:
        app.wsgi_app = ProxyFix(  # type: ignore[assignment]
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        # Local development is done over HTTP, not HTTPS.
        SESSION_COOKIE_SECURE=not app.config.get("DEBUG", False),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(days=28),
    )


def register_blueprints(app: Flask, settings: WsgiSettings) -> None:
    app.register_blueprint(streams, url_prefix="/")

    app.auth_links = []  # type: ignore[attr-defined]
    app.register_blueprint(auth, url_prefix="/auth")

    if settings.TOTP:
        from no_comment.infrastructure.flask.totp import blueprint as totp

        app.register_blueprint(totp, url_prefix="/auth/totp")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "totp.login", "label": "TOTP"}
        )

    if settings.AUTHORIZED_IP:
        from no_comment.infrastructure.flask.ip import blueprint as ip

        app.register_blueprint(ip, url_prefix="/auth/ip")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "ip.login", "label": "IP"}
        )


def register_globals(settings: WsgiSettings) -> None:
    html_presenters.register_jinja_global("version", __version__)
    html_presenters.register_jinja_global("url_for", url_for)
    html_presenters.register_jinja_global("get_flashed_messages", get_flashed_messages)
    html_presenters.register_jinja_global("timezone", settings.TIMEZONE)
