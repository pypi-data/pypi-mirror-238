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

from typing import Callable

from no_comment.application.use_cases import create_stream
from no_comment.domain.commenting.entities import Stream
from no_comment.interfaces.to_terminal import TerminalPresenter


class CreateStream(TerminalPresenter, create_stream.Presenter):
    def __init__(self, printer: Callable[[str], None]) -> None:
        self.__print = printer
        self.__exit_code = 1

    def exit_code(self) -> int:
        return self.__exit_code

    def bad_parameter(self, message: str) -> None:
        self.__print(f"[BAD PARAMETER] {message}")
        self.__exit_code = 1

    def stream_already_exists(self, stream: Stream) -> None:
        self.__print("Stream already exists!")
        self.__exit_code = 2

    def stream_created(self, stream: Stream) -> None:
        self.__print("Stream created!")
        self.__exit_code = 0
