#!/usr/bin/env python3
"""A command line interface framework."""

import argparse

from . import protocols, _wrappers
from .protocols import Command, SingleCommand, GroupCommand, PrintFn

__all__ = ["main", "Command", "SingleCommand", "GroupCommand", "PrintFn"]


def main(commands: list[protocols.Command], **parser_kwargs):
    """The main entry point for the command line interface framework."""
    # Create the main parser
    parser = argparse.ArgumentParser(**parser_kwargs)
    # Global arguments
    parser.add_argument(
        "--logfile", type=str, default="/dev/stdout", help="The logging output file."
    )
    # Wrap up command with internal helpers
    cmds = [_wrappers.wrap(command) for command in commands]
    cmds_by_name: dict[str, _wrappers.WrapperBase] = {
        cmd.get_name(): cmd for cmd in cmds
    }
    # Add the subcommand arguments to the parser
    subparsers = parser.add_subparsers(dest="command", required=True)
    for cmd in cmds:
        cmd.add_arguments(subparsers)
    # Parse the arguments
    args = parser.parse_args()
    command_name = args.command
    cmd = cmds_by_name[command_name]
    # Run the command
    with open(args.logfile, "w") as file:

        def print_fn(*args) -> None:
            strs = map(str, args)
            file.write(" ".join(strs) + "\n")

        cmd.run(args, print_fn)
