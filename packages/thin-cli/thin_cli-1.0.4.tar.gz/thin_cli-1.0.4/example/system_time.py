import argparse
import datetime

import thin_cli


class Time:
  """List directory contents"""
  @staticmethod
  def __cli_add_arguments__(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--show_24_hour", "--24", action="store_true", help="Show 24 hour time")
    parser.add_argument("--utc", "-u", action="store_true", help="Use UTC as the timezone")

  @staticmethod
  def __cli_run__(args: argparse.Namespace, print_fn: thin_cli.PrintFn) -> None:
    if args.utc:
      current_time = datetime.datetime.utcnow()
    else:
      current_time = datetime.datetime.now()

    if args.show_24_hour:
      time_format = "%H:%M:%S"
    else:
      time_format = "%I:%M:%S %p"

    formatted_time = current_time.strftime(time_format)
    print_fn(formatted_time)
