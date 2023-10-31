#!/usr/bin/env python3
import thin_cli

from example import file_system, system_time

if __name__ == "__main__":
    thin_cli.main([file_system.FS, system_time.Time])