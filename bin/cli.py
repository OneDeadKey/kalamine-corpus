from contextlib import contextmanager
from importlib import metadata
from pathlib import Path
from typing import Iterator, List, Literal, Union

import click
import chardict as corpus

@click.group()
def cli() -> None: ...

@cli.command()
@click.argument("filename")
@click.option("-n",
              "--name",
              default="",
              type=str,
              help="Define corpus name",
)
@click.option("-c",
            "--encoding",
            default="utf-8",
            type=str)
def add(filename, name, encoding):
    corpus.add(filename, name, encoding)

@cli.command()
@click.argument("name")
def rm(name):
    corpus.rm(name)


# @cli.command()
# def version() -> None:
#     """Show version number and exit."""
#     click.echo(f"kalamine { metadata.version('kalamine') }")


if __name__ == "__main__":
    cli()