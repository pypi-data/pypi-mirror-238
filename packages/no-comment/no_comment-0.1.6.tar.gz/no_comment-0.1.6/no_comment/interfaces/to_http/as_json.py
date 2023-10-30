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

import json
from http import HTTPStatus as HTTP
from typing import Any

from no_comment.application.use_cases import add_comment, display_stream
from no_comment.domain.commenting import entities, value_objects
from no_comment.interfaces.to_http import HttpPresenter


class JsonPresenter(HttpPresenter):
    def __init__(self) -> None:
        self.__status_code: HTTP = HTTP.OK
        self.__headers: dict[str, str] = {"Content-Type": "application/json"}
        self.__data: str = ""

    def status_code(self) -> int:
        return int(self.__status_code)

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.__data


class DisplayStreamAsJsonFeed(display_stream.Presenter, JsonPresenter):
    def __init__(self, url_self: str, url_alternate: str) -> None:
        super().__init__()
        self.__data: dict[str, Any] = {
            "version": "https://jsonfeed.org/version/1.1",
            "home_page_url": url_alternate,
            "feed_url": url_self,
            "items": [],
        }
        self.__error = ""

    def data(self) -> str:
        if self.__error:
            return ""

        return json.dumps(self.__data)

    def bad_request(self) -> None:
        self.__error = "bad request"
        self.set_status_code(HTTP.BAD_REQUEST)

    def unknown_stream(self, stream_id: value_objects.StreamId) -> None:
        self.__error = "unknown stream"
        self.set_status_code(HTTP.NOT_FOUND)

    def stream(self, stream: entities.Stream) -> None:
        self.__data["title"] = str(stream.title)
        self.__data["description"] = str(stream.description)
        self.__data["authors"] = [{"name": str(stream.author)}]

    def comment(self, comment: entities.Comment) -> None:
        self.__data["items"].append(
            {
                "id": "ID",
                "content_html": str(comment.text),
                "content_text": str(comment.text),
                "url": str(comment.url),
                "date_published": comment.created_at.to_isoformat(),
            }
        )


class AddComment(add_comment.Presenter, JsonPresenter):
    def __init__(self) -> None:
        super().__init__()
        self.__status_code = HTTP.NOT_IMPLEMENTED
        self.__data: dict[str, Any] = {}

    def status_code(self) -> int:
        return int(self.__status_code)

    def data(self) -> str:
        return json.dumps(self.__data)

    def bad_parameter(self, name: str, value: str) -> None:
        self.__status_code = HTTP.BAD_REQUEST
        self.__data = {"error": {name: value}}

    def comment_added(self, comment: entities.Comment) -> None:
        self.__status_code = HTTP.CREATED
        # TODO return comment's data!?
