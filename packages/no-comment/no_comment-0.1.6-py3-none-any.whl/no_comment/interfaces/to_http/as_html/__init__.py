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

from datetime import datetime
from http import HTTPStatus as HTTP
from pathlib import Path
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2_fragments import render_block

from no_comment.application.use_cases import add_comment, display_stream
from no_comment.domain.commenting import entities, value_objects
from no_comment.interfaces import Pager, User
from no_comment.interfaces.to_http import HttpPresenter

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
)
ENVIRONMENT.globals["timezone"] = "Europe/Paris"


def register_jinja_global(key: str, value: Any) -> None:
    ENVIRONMENT.globals[key] = value


def format_datetime(dt: datetime) -> str:
    z = ZoneInfo(str(ENVIRONMENT.globals["timezone"]))
    return dt.astimezone(z).strftime("%Y-%m-%d %H:%M:%S")


class JinjaPresenter(HttpPresenter):
    def __init__(self, template: str, /, *, fragment: str = "", **context: Any) -> None:
        self.__status_code = HTTP.OK
        self.__headers = {"Content-Type": "text/html; charset=UTF-8"}
        self.__template = template
        self.__fragment = fragment
        self.__context = context
        self.__error = ""

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def status_code(self) -> int:
        return int(self.__status_code)

    def set_header(self, name: str, value: str) -> None:
        self.__headers[name] = value

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.render()

    def error(self, message: str, status_code: HTTP) -> None:
        self.__error = message
        self.__status_code = status_code

    def access_not_allowed(self, login: str) -> None:
        if login:
            self.__status_code = HTTP.FORBIDDEN
            self.__error = "You cannot access this page!"
        else:
            self.__status_code = HTTP.UNAUTHORIZED
            self.__error = "You must be logged in to access this page!"

    def set_template(self, template: str, fragment: str = "") -> None:
        self.__template = template
        self.__fragment = fragment

    def render(self, **context: Any) -> str:
        if self.__error:
            return ENVIRONMENT.get_template("error.pug").render(
                **self.__context,
                **context,
                message=self.__error,
            )
        if self.__fragment:
            return render_block(  # type: ignore
                ENVIRONMENT,
                self.__template,
                self.__fragment,
                **self.__context,
                **context,
            )
        return ENVIRONMENT.get_template(self.__template).render(
            **self.__context, **context
        )


class PugPresenter(JinjaPresenter):
    def __init__(self, template: str, **context: Any) -> None:
        super().__init__(template + ".pug", **context)

    def set_template(self, template: str, fragment: str = "") -> None:
        super().set_template(template + ".pug", fragment)


class UnknownFormat(display_stream.Presenter, HttpPresenter):
    def __init__(self, url: str) -> None:
        self.__url = url

    def status_code(self) -> int:
        return HTTP.SEE_OTHER

    def headers(self) -> dict[str, str]:
        return {"Location": self.__url}

    def data(self) -> str:
        return ""

    def bad_request(self) -> None:
        pass

    def unknown_stream(self, stream_id: value_objects.StreamId) -> None:
        pass

    def stream(self, stream: entities.Stream) -> None:
        pass

    def comment(self, comment: entities.Comment) -> None:
        pass


class DisplayStream(display_stream.Presenter, PugPresenter):
    def __init__(
        self,
        url: str,
        /,
        *,
        fragment: str = "",
        filter: str = "",
        user: Optional[User] = None,
    ) -> None:
        super().__init__("streams/display", fragment=fragment, user=user)
        self.__context: dict[str, Any] = {
            "text_max_length": str(value_objects.Text.MAX),
            "stream": {"title": "?", "description": "?", "author": "?"},
            "comments": [],
            "filter": filter,
            "pager": Pager(url),
            "error": "",
        }

    def bad_request(self) -> None:
        self.__context["error"] = "bad request"
        self.set_status_code(HTTP.BAD_REQUEST)

    def unknown_stream(self, stream_id: value_objects.StreamId) -> None:
        self.set_status_code(HTTP.NOT_FOUND)
        self.set_template("streams/unknown")

    def stream(self, stream: entities.Stream) -> None:
        self.__context["stream"] = {
            "id": str(stream.id),
            "title": str(stream.title),
            "description": str(stream.description),
            "author": str(stream.author),
        }

    def comment(self, comment: entities.Comment) -> None:
        self.__context["comments"].append(
            {
                "url": str(comment.url),
                "text": self.__format_text(str(comment.text)),
                "created_at": format_datetime(comment.created_at.to_datetime()),
            },
        )

    def __format_text(self, text: str) -> str:
        # Hashes are use for tags, not for titles!
        return markdown.markdown(text.replace("#", "\\#"))

    def render(self, **context: Any) -> str:
        self.__context["comments"] = sorted(
            self.__context["comments"],
            key=lambda c: str(c["created_at"]),
            reverse=True,
        )
        return super().render(**self.__context, **context)


class DisplayComment(PugPresenter):
    def __init__(self) -> None:
        super().__init__("streams/comment_display")


class AddComment(PugPresenter, add_comment.Presenter):
    def __init__(
        self,
        data: dict[str, str],
        next_url: Callable[[], str],
        /,
        *,
        filter: str = "",
        fragment: str = "",
    ) -> None:
        super().__init__("streams/display", fragment=fragment)
        self.__next_url = next_url
        self.__fragment = fragment
        self.__context = {
            "text_max_length": str(value_objects.Text.MAX),
            "filter": filter,
            "url": data.get("url", ""),
            "text": data.get("text", ""),
            "comment_id": "",
            "error": "",
        }

    def status_code(self) -> int:
        if self.__fragment:
            return HTTP.OK
        return HTTP.SEE_OTHER

    def headers(self) -> dict[str, str]:
        if self.__fragment and self.__context["comment_id"]:
            return {"HX-Trigger": "commentAdded"}
        return {"Location": self.__next_url()}

    def data(self) -> str:
        if self.__fragment:
            return super().render(**self.__context)
        return ""

    def bad_parameter(self, name: str, value: str) -> None:
        self.__context["error"] = f"Missing {name}!"

    def comment_added(self, comment: entities.Comment) -> None:
        self.__context["comment_id"] = str(comment.id)
        self.__context["url"] = ""
        self.__context["text"] = ""
