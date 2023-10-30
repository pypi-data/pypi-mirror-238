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

from flask import Blueprint, Response, request, url_for

from no_comment.application.use_cases import add_comment, display_stream
from no_comment.infrastructure.flask.utils import htmx, presenter_to_response
from no_comment.interfaces import Pager
from no_comment.interfaces.to_http import as_html as html_presenters
from no_comment.interfaces.to_http import as_json as json_presenters
from no_comment.interfaces.to_http import as_xml as xml_presenters

from . import services

blueprint = Blueprint("streams", __name__)


@blueprint.get("/")
@presenter_to_response
def root() -> Response:
    return html_presenters.PugPresenter(
        "streams/root", streams=services.get_streams().all()
    )


@blueprint.get("/<string:stream_id>")
@blueprint.get("/<string:stream_id>.<string:format>")
@presenter_to_response
def display(stream_id: str, format: str = "html") -> Response:
    presenter = select_presenter_for_display_stream(
        stream_id, format, request.args.get("url", "")
    )
    interactor = display_stream.Interactor(
        presenter, services.get_streams(), services.get_comments()
    )
    rq = display_stream.Request(
        stream_id,
        request.args.get("url"),
        int(request.args.get("page", "1")),
        Pager.PAGE_SIZE,
    )
    interactor.execute(rq)
    return presenter


def select_presenter_for_display_stream(
    stream_id: str, format: str, filter: str
) -> display_stream.Presenter:
    url_self = url_for(
        "streams.display", stream_id=stream_id, format=format, _external=True
    )
    url_alternate = url_for("streams.display", stream_id=stream_id, _external=True)

    PRESENTERS = {
        "html": html_presenters.DisplayStream(
            request.url, user=services.get_user(), fragment=htmx.target, filter=filter
        ),
        "atom": xml_presenters.DisplayStreamAsAtom(url_self, url_alternate),
        "rss": xml_presenters.DisplayStreamAsRss(url_self, url_alternate),
        "json": json_presenters.DisplayStreamAsJsonFeed(url_self, url_alternate),
    }
    return PRESENTERS.get(format, html_presenters.UnknownFormat(url_alternate))


@blueprint.post("/<string:stream_id>")
@presenter_to_response
def comment_add(stream_id: str) -> Response:
    presenter = html_presenters.AddComment(
        request.form,
        lambda: url_for("streams.display", stream_id=stream_id),
        fragment=htmx.target,
        filter=request.args.get("url", ""),
    )
    interactor = add_comment.Interactor(
        presenter, services.get_comments(), services.get_calendar()
    )
    rq = add_comment.Request(
        stream_id, request.form.get("url", ""), request.form.get("text", "")
    )
    interactor.execute(rq)
    return presenter


@blueprint.get("/<string:stream_id>/<string:comment_id>")
@presenter_to_response
def comment_display(stream_id: str, comment_id: str) -> Response:
    return html_presenters.DisplayComment()
