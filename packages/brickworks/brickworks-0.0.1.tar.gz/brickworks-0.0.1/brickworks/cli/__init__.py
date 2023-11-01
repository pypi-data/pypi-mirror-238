import importlib
import os
import sys
from ast import mod
from functools import lru_cache
from math import e
from typing import Optional

import tomli
import typer
from typing_extensions import Annotated

from brickworks.cli import db_migration
from brickworks.settings import BrickworksSettings
from brickworks.utils.loader import import_object_from_path

app = typer.Typer()


current_working_directory = os.getcwd()
sys.path.append(current_working_directory)


def _get_settings(path: str = "pyproject.toml") -> BrickworksSettings:
    """
    Tries to import the settings object.
    If a settings path is specified in the pyproject.toml, it will try to import the settings object from there.
    The path is specified in the "tool.brickworks.settings" key and should be a string like
    "settingsmodule.settingsobject".

    If the path is not specified it will try to import the settings object from settings.settings.
    """
    attribute_path = _get_tool_config(path).get("settings") or "settings.settings"

    try:
        settings = import_object_from_path(attribute_path)
    except ImportError as exc:
        typer.echo("Could not find settings.py")
        raise typer.Exit(code=1) from exc
    except AttributeError as exc:
        typer.echo(f"Could not find {attribute_path} in settings.py")
        raise typer.Exit(code=1) from exc

    return settings


@lru_cache(maxsize=1)
def _get_tool_config(path: str = "pyproject.toml"):
    """
    Tries to import pyproject.toml from the current working directory and returns the "tool.brickworks" settings.
    """
    try:
        with open(path, "rb") as f:
            settings = tomli.load(f)
    except FileNotFoundError as exc:
        typer.echo(f"Could not find {path}")
        raise typer.Exit(code=1) from exc
    return settings.get("tool", {}).get("brickworks", {})


@app.command()
def migrate():
    """Run database migrations."""
    typer.echo("Migrating database")
    db_migration.migrate(_get_settings())


@app.command()
def make_migration(message: Annotated[Optional[str], typer.Argument()] = None):
    """Create a new database migration."""
    if not db_migration.has_changes(_get_settings()):
        raise typer.Exit(code=0)
    message = message or ""
    typer.echo(f"Creating migration with message: {message}")
    db_migration.make_migration(_get_settings(), message)


def main():
    app()


if __name__ == "__main__":
    main()
