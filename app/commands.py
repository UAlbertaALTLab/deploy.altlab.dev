#!/usr/bin/env python3

"""
What to do on a deploy.
"""

from subprocess import check_call


class ConnectTo:
    """
    Connects to the given server via SSH, then runs the given command.

    Usage:

        ConnectTo("server.address.com")\
            .command("/path/to/your/command")

    """

    def __init__(self, server_name: str) -> None:
        self.server_name = server_name

    def command(self, *args) -> "ConnectTo":
        self.command_args = args
        return self

    def run(self) -> None:
        check_call(["ssh", self.server_name, *self.command_args])
