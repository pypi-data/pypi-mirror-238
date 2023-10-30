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

from pathlib import Path
from typing import Any

import click
from sqlalchemy import create_engine

from no_comment import __version__
from no_comment.application.use_cases import create_stream
from no_comment.infrastructure.click import commands, services
from no_comment.infrastructure.settings import CliSettings
from no_comment.infrastructure.sqlalchemy.repositories import META_DATA
from no_comment.interfaces.to_terminal import as_text as presenters


@click.group()
def cli() -> Any:
    pass


@cli.command()  # type: ignore
@click.pass_context
def version(ctx: click.Context) -> None:
    click.echo(__version__)
    ctx.exit(0)


@cli.command()  # type: ignore
@click.pass_context
def init_db(ctx: click.Context) -> None:
    """Initialise database's schema."""
    click.echo("Initialising schema…", nl=False)
    engine = create_engine(ctx.obj.DSN)
    META_DATA.create_all(engine)
    click.echo(" OK!")
    ctx.exit(0)


@cli.group()  # type: ignore
def streams() -> None:
    pass


@streams.command()  # type: ignore
@click.argument("id")
@click.argument("title")
@click.argument("description", default="")
@click.argument("author", default="anonymous")
@click.pass_context
def create(
    ctx: click.Context, id: str, title: str, author: str, description: str
) -> None:
    """Create a new stream."""
    presenter = presenters.CreateStream(click.echo)
    request = create_stream.Request(id, title, description, author)

    with services.get_connection(ctx.obj) as connection:
        interactor = create_stream.Interactor(
            presenter, services.get_streams(connection), services.get_calendar()
        )
        interactor.execute(request)

    ctx.exit(presenter.exit_code())


def build_cli(settings: CliSettings) -> Any:
    return cli(obj=settings)  # type: ignore


@cli.command()  # type: ignore
@click.argument("comments")
@click.argument("created")
@click.pass_context
def convert(ctx: click.Context, comments: str, created: str) -> None:
    """Import data from the old Markdown format.

    $ no-comment convert PATH_TO/commentaires.md PATH_TO/created.txt > comments.jsons

    `created.txt` contains timestamps and URLs.
    """

    commands.convert(Path(comments), Path(created))
    ctx.exit(0)


@cli.command()  # type: ignore
@click.argument("comments")
@click.argument("categories", nargs=-1)
@click.pass_context
def dispatch(ctx: click.Context, comments: str, categories: list[str]) -> None:
    """Dispatch comments.

    $ no-comment dispatch comments.jsons informatique culture societe covid autre
    """

    commands.dispatch_comments(Path(comments), categories)
    ctx.exit(0)


@cli.command()  # type: ignore
@click.argument("stream")
@click.pass_context
def import_to(ctx: click.Context, stream: str) -> None:
    """Import comments to a given STREAM."""

    with services.get_connection(ctx.obj) as connection:
        commands.import_to(
            services.get_streams(connection),
            stream,
            services.get_comments(connection),
        )
    ctx.exit(0)


@cli.command()  # type: ignore
@click.argument("stream")
@click.pass_context
def export_from(ctx: click.Context, stream: str) -> None:
    """Export comments from a given STREAM."""

    with services.get_connection(ctx.obj) as connection:
        commands.export_from(
            services.get_streams(connection),
            stream,
            services.get_comments(connection),
        )
    ctx.exit(0)
