import argparse
import os

import thin_cli

class LS:
  """List directory contents"""
  @staticmethod
  def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", type=str)
    parser.add_argument("--recursive", "-r", action="store_true")

  @staticmethod
  def __cli_run__(args: argparse.Namespace, print_fn: thin_cli.PrintFn) -> None:
    if args.recursive:
      LS._list_recursive(args.path, print_fn)
    else:
      for path in os.listdir(args.path):
        print_fn(path)

  @staticmethod
  def _list_recursive(directory: str, print_fn: thin_cli.PrintFn, indent="") -> None:
    next_indent = "  " + indent
    for path in os.listdir(directory):
      print_fn(indent+path)
      if os.path.isdir(path):
        LS._list_recursive(path, print_fn, next_indent)


class Cat:
  """Concatenate and print files"""
  @staticmethod
  def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('files', metavar='file', type=str, nargs='+', help='The files to concatenate and display')

  @staticmethod
  def __cli_run__(args: argparse.Namespace, print_fn: thin_cli.PrintFn) -> None:
    for file in args.files:
      with open(file, 'r') as f:
        contents = f.read()
        print_fn(contents)


class FS:
  """Interact with the file system."""

  @staticmethod
  def __cli_subcommands__() -> list[thin_cli.Command]:
    return [LS, Cat]

  @staticmethod
  def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
    pass
