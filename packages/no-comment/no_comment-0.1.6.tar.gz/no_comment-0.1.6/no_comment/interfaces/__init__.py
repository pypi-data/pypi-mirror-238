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
from urllib.parse import urlparse


@dataclass
class User:
    user_id: str


class Pager:
    # Should be divisible by 2 and 3 for rows to always be complete.
    PAGE_SIZE = 12

    def __init__(self, url: str) -> None:
        self.__url = urlparse(url)
        self.previous = self.__previous_page()
        self.next = self.__next_page()

    def __previous_page(self) -> str:
        page = self.__get_page()
        if page < 2:
            return ""
        return self.__set_page(page - 1)

    def __get_page(self) -> int:
        for q in self.__get_query():
            if q[0] == "page":
                if q[1].isnumeric():
                    return int(q[1])
        return 1

    def __get_query(self) -> list[list[str]]:
        return [q.split("=", 1) for q in self.__url.query.split("&")]

    def __set_page(self, page: int) -> str:
        if not page:
            return ""
        page_replaced = False
        query = []
        for q in self.__get_query():
            if q[0] == "page":
                query.append(f"page={page}")
                page_replaced = True
            else:
                query.append("=".join(q))
        if not page_replaced:
            query.append(f"page={page}")
        return self.__url._replace(query="&".join(query)).geturl()

    def __next_page(self) -> str:
        return self.__set_page(self.__get_page() + 1)
