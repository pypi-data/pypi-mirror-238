#!/usr/bin/env python3
from __future__ import annotations

import json as json_mod
import logging
import os
import subprocess
import sys
from functools import lru_cache, wraps
from pathlib import Path
from typing import Callable

import click
from tabulate import tabulate
from toolforge_weld.config import Config

from toolforge_envvars_cli.config import get_loaded_config
from toolforge_envvars_cli.envvars import EnvvarsClient, EnvvarsClientError

LOGGER = logging.getLogger("toolforge" if __name__ == "__main__" else __name__)


def _with_nice_error(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except EnvvarsClientError as error:
            click.echo(err=True, message=click.style(error.to_str(), fg="red"))
            sys.exit(1)

    return _inner


def _format_headers(headers: list[str]) -> list[str]:
    return [click.style(item, bold=True) for item in headers]


@lru_cache(maxsize=None)
def _load_config_from_ctx() -> Config:
    ctx = click.get_current_context()
    return ctx.obj["config"]


def shared_options(func: Callable) -> Callable:
    @click.option(
        "--kubeconfig",
        hidden=True,
        default=Path(os.environ.get("KUBECONFIG", "~/.kube/config")),
        type=Path,
    )
    @_with_nice_error
    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        return func(*args, **kwargs)

    return wrapper


@click.version_option(prog_name="Toolforge envvars CLI")
@click.group(name="toolforge", help="Toolforge command line")
@click.option(
    "-v",
    "--verbose",
    help="Show extra verbose output. NOTE: Do no rely on the format of the verbose output",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_VERBOSE", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.option(
    "-d",
    "--debug",
    help=(
        "show logs to debug the toolforge-envvars-* packages. For extra verbose output for say build or "
        "job, see --verbose"
    ),
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_DEBUG", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.pass_context
def toolforge_envvars(ctx: click.Context, verbose: bool, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["config"] = get_loaded_config()
    pass


@toolforge_envvars.command(name="list", help="List all your envvars.")
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@click.option(
    "--truncate",
    help="If set, will truncate long envvar values. Defaults to True.",
    is_flag=True,
    default=True,
)
@shared_options
def envvar_list(
    kubeconfig: Path,
    json: bool = False,
    truncate: bool = True,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config, kubeconfig=kubeconfig)
    envvars = envvars_client.get("/envvar")

    if json:
        click.echo(json_mod.dumps(envvars, indent=4))
    else:
        formatted_envvars = [
            [envvar["name"], envvar["value"][:50] if truncate else envvar["value"]] for envvar in envvars
        ]

        click.echo(
            tabulate(
                formatted_envvars,
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="show", help="Show a specific envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@shared_options
def envvar_show(
    kubeconfig: Path,
    envvar_name: str,
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config, kubeconfig=kubeconfig)
    envvar = envvars_client.get(f"/envvar/{envvar_name}")

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="create", help="Create/update an envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.argument("ENVVAR_VALUE", required=True)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@shared_options
def envvar_create(
    kubeconfig: Path,
    envvar_name: str,
    envvar_value: str,
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config, kubeconfig=kubeconfig)
    envvar = envvars_client.post(f"/envvar/{envvar_name}", json={"value": envvar_value})

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="delete", help="Delete an envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
@shared_options
def envvar_delete(
    kubeconfig: Path,
    envvar_name: str,
    json: bool = False,
    yes_im_sure: bool = False,
) -> None:
    config = _load_config_from_ctx()

    if not yes_im_sure:
        if not click.prompt(
            text=f"Are you sure you want to delete {envvar_name}? (this can't be undone) [yN]",
            default="no",
            show_default=False,
            type=lambda val: val.lower() in ["y", "Y", "1", "yes", "true"],
        ):
            click.echo("Aborting at user's request")
            sys.exit(1)

    envvars_client = EnvvarsClient.from_config(config=config, kubeconfig=kubeconfig)
    envvar = envvars_client.delete(f"/envvar/{envvar_name}")

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(f"Deleted {envvar_name}, here it's it's last value:")
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="quota", help="Get envvars quota information.")
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@shared_options
def envvar_quota(
    kubeconfig: Path,
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config, kubeconfig=kubeconfig)
    quota = envvars_client.get("/quota")

    if json:
        click.echo(json_mod.dumps(quota, indent=4))
    else:
        formatted_quota = [[quota["quota"], quota["used"], quota["quota"] - quota["used"]]]

        click.echo(
            tabulate(
                formatted_quota,
                headers=_format_headers(["quota", "used", "available"]),
                tablefmt="plain",
            )
        )


def main() -> int:
    # this is needed to setup the logging before the subcommand discovery
    res = toolforge_envvars.parse_args(ctx=click.Context(command=toolforge_envvars), args=sys.argv)
    if "-d" in res or "--debug" in res:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        toolforge_envvars()
    except subprocess.CalledProcessError as err:
        return err.returncode

    return 0


if __name__ == "__main__":
    main()
