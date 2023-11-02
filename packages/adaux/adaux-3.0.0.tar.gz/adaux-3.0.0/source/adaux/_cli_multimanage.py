# Copyright (c) 2021-2023 Mario S. Könz; License: MIT
import shlex
import typing as tp

import click

from ._cli import adaux
from ._cli import convert_runtime_to_click_error


@adaux.group()  # type: ignore
@click.pass_context
def mm(ctx) -> None:  # pylint: disable=unused-argument
    """
    Allows to run adaux or bash commands over multiple adaux projects.
    """


@mm.command()  # type: ignore
@click.pass_context
@click.option(
    "-a",
    "--all-vip-branches",
    is_flag=True,
    default=False,
    help="update all vip branches",
)
@click.option(
    "-p",
    "--prune",
    is_flag=True,
    default=False,
    help="prunes local branches that are not on remote",
)
def update(ctx, all_vip_branches: tp.Tuple[str, ...], prune) -> None:
    with convert_runtime_to_click_error(ctx):
        with ctx.obj.extra():
            ctx.obj.mm_update(all_vip_branches, prune)


@mm.command()  # type: ignore
@click.pass_context
@click.argument("cmd_parts", nargs=-1)
def run(ctx, cmd_parts: tp.Tuple[str]) -> None:
    with convert_runtime_to_click_error(ctx):
        with ctx.obj.extra():
            if len(cmd_parts) > 1:
                cmd_str = shlex.join(cmd_parts)
            else:
                cmd_str = cmd_parts[0]
            ctx.obj.mm_run(cmd_str)


@mm.command()  # type: ignore
@click.pass_context
@click.argument("cmd_parts", nargs=-1)
def a(ctx, cmd_parts: tp.Tuple[str]) -> None:
    with convert_runtime_to_click_error(ctx):
        with ctx.obj.extra():
            if len(cmd_parts) > 1:
                cmd_str = shlex.join(cmd_parts)
            else:
                cmd_str = cmd_parts[0]
            ctx.obj.mm_adaux(cmd_str)
