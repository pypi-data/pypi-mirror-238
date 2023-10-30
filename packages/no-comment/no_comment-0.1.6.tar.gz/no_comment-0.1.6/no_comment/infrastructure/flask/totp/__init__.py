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

from typing import Any, cast

import pyotp
from flask import Blueprint, flash, request, session, url_for

from no_comment.infrastructure.flask import services
from no_comment.infrastructure.flask.utils import presenter_to_response
from no_comment.infrastructure.settings import TotpSettings
from no_comment.interfaces.to_http import Redirection, as_html

blueprint = Blueprint("totp", __name__)


@blueprint.get("/login")
@presenter_to_response
def login() -> Any:
    return as_html.PugPresenter("totp/login", user=services.get_user())


@blueprint.post("/login")
@presenter_to_response
def login_POST() -> Any:
    # TOTP settings must be defined for this route to be accessible.
    # Other alternatives: 1) check presence with `if` or 2) ignore type.
    TOTP = cast(TotpSettings, services.get_settings().TOTP)

    totp = pyotp.TOTP(TOTP.SECRET)
    if not totp.verify(request.form.get("password", "")):
        flash("Error authenticating with TOTP.", "error")
        return Redirection(url_for("totp.login"))

    session["user_id"] = "anonymous"

    flash("Success authenticating with TOTP.", "success")
    return Redirection(url_for("auth.redirect"))
