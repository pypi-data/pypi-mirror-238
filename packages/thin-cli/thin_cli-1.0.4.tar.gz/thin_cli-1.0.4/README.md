# Thin CLI
A command line interface framework.

# How to use

## Define your `Command`
For each command you would like to define, create a class (possibly in its own
python file) that follows the `thin_cli.Command` type. It needs to implement
two static methods: one to configure argparse and one to run.

For an example, see the `example` folder which implements a `time` command and
a `fs` (file system) command with subcommands `cat` and `ls`.

## Call `thin_cli.main`
At your entrypoint, all you need to do is call `thin_cli.main` with the list of
`thin_cli.Command` classes.

```python
import thin_cli

from file_system import FS
from system_time import Time

if __name__ == "__main__":
  thin_cli.main([FS, Time])
```