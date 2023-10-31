import abc
import argparse

from . import protocols

SubParsers = argparse._SubParsersAction


class WrapperBase(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_doc(self) -> str:
        ...

    @abc.abstractmethod
    def add_arguments(self, parent_parsers: SubParsers) -> None:
        ...

    @abc.abstractmethod
    def run(self, args: argparse.Namespace, print_fn: protocols.PrintFn) -> None:
        ...


class SingleWrapper(WrapperBase):
    def __init__(self, cmd: protocols.SingleCommand):
        assert isinstance(cmd, type), f"Expected {cmd} to be a class."
        assert issubclass(
            cmd, protocols.SingleCommandProtocol
        ), f"Expected {cmd} to be implement SingleCommandProtocol."
        self.cmd = cmd
        self.name = cmd.__name__.lower()

    def get_name(self):
        return self.name

    def get_doc(self):
        if hasattr(self.cmd, "__doc__") and self.cmd.__doc__:
            return self.cmd.__doc__.splitlines()[0]
        else:
            return ""

    def add_arguments(self, parent_parsers):
        parser = parent_parsers.add_parser(self.get_name(), help=self.get_doc())
        self.cmd.__cli_add_arguments__(parser)

    def run(self, args, print_fn):
        self.cmd.__cli_run__(args, print_fn)


class GroupWrapper(WrapperBase):
    class CustomSubParsersAction(argparse._SubParsersAction):
        def __init__(self, *args, group_wrapper: "GroupWrapper", **kwargs):
            super().__init__(*args, **kwargs)
            self.group_wrapper = group_wrapper

        def __call__(self, parser, namespace, values, option_string=None):
            self.group_wrapper.sub_cmd = values[0]
            super().__call__(parser, namespace, values, option_string)

    def __init__(self, cmd: protocols.GroupCommand):
        assert isinstance(cmd, type), f"Expected {cmd} to be a class."
        assert issubclass(
            cmd, protocols.GroupCommandProtocol
        ), f"Expected {cmd} to be implement GroupCommandProtocol."
        self.cmd = cmd
        self.name = cmd.__name__.lower()
        cmd_list = [wrap(sub_cmd) for sub_cmd in cmd.__cli_subcommands__()]
        self.cmds: dict[str, WrapperBase] = {
            sub_cmd.get_name(): sub_cmd for sub_cmd in cmd_list
        }
        self.sub_cmd = None

    def get_name(self):
        return self.name

    def get_doc(self):
        if hasattr(self.cmd, "__doc__") and self.cmd.__doc__:
            return self.cmd.__doc__.splitlines()[0]
        else:
            return ""

    def add_arguments(self, parent_parsers):
        parser = parent_parsers.add_parser(self.get_name(), help=self.get_doc())
        self.cmd.__cli_add_arguments__(parser)
        subparsers = parser.add_subparsers(
            title=self.get_name(),
            dest="subcommand",
            group_wrapper=self,
            required=True,
            action=self.CustomSubParsersAction,
        )
        for sub_cmd in self.cmds.values():
            sub_cmd.add_arguments(subparsers)

    def run(self, args, print_fn):
        print("sub_cmd_name", self.sub_cmd)
        self.cmds[self.sub_cmd].run(args, print_fn)


def wrap(cmd: protocols.Command) -> WrapperBase:
    assert isinstance(cmd, type), f"Expected {cmd} to be a class."
    if issubclass(cmd, protocols.SingleCommandProtocol):
        return SingleWrapper(cmd)
    if issubclass(cmd, protocols.GroupCommandProtocol):
        return GroupWrapper(cmd)
