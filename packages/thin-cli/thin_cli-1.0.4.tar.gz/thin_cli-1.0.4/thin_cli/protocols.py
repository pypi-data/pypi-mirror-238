#!/usr/bin/env python3
"""Defines subcommands and command groups for the command line interface framework."""

import argparse
from typing import Callable, runtime_checkable, Protocol, Type, Union

SingleCommand = Type["SingleCommandProtocol"]
GroupCommand = Type["GroupCommandProtocol"]
Command = Union[SingleCommand, GroupCommand]
"""A Command is a class object that fulfills one of the Command protocols.

The name of the Command from the command line will be the name of the class in
lowercase. If possible, the argparse help string defaults to the first line of
class's docstring.

The two protocols are SingleCommandProtocol and GroupCommandProtocol.

A SingleCommand must be able to add its parameter arguments to a parser object,
and it must be able to run itself with the parsed arguments.

A GroupCommand must be able to list its subcommands as well as add any shared
parameter arguments to a parser object

To add a new Command, create a class, implement these two static methods, and
add the class to the list of commands when calling `thin_cli.main(...)`.
"""

PrintFn = Callable[..., None]
"""The type signature of the `print` function."""


@runtime_checkable
class SingleCommandProtocol(Protocol):
    """The Protocol for a command to be runnable from the command line."""

    @staticmethod
    def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
        """Adds the CLI arguments for this command to an argparse parser."""

    @staticmethod
    def __cli_run__(args: argparse.Namespace, print_fn: PrintFn) -> None:
        """Runs this command with the given CLI arguments and printer."""


@runtime_checkable
class GroupCommandProtocol(Protocol):
    """The Protocol for a group of commands to be runnable from the command line."""

    @staticmethod
    def __cli_subcommands__() -> list[Command]:
        """Returns a list of subcommands forming the group."""

    @staticmethod
    def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
        """Adds the shared CLI arguments in common for this command group to an argparse parser."""
