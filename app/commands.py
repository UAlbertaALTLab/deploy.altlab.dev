"""
What to do on a deploy.
"""

from subprocess import check_call
from abc import ABC, abstractmethod


class Command:
    """
    Implements the commmand pattern.
    """

    @abstractmethod
    def run(self) -> None:
        """
        This should complete the deployment.
        """


class ConnectTo(Command):
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


class NotConfigured(Command):
    def run(self) -> None:
        raise NotImplementedError("Deployment not configured")


class RedeploySelf(Command):
    """
    How deploy.altlab.app re-deploys *itself*.
    """

    # This is how this app assumes it's configured:
    #
    #  - It can `git pull` itself
    #  - It has a systemd unit file (service) that manages it.
    #  - The unit file has ExecReload configured to gracefully reload the app.
    #  - The user running the code can issue the systemd reload command to itself.

    # systemd unit name. Check /etc/systemd/system!
    UNIT_NAME = "deploy.altlab.dev"

    def run(self) -> None:
        check_call(["git", "pull", "--ff-only"])
        # Note: Make sure the user running this app is allowed to run this command
        # without a password. Add something like this to the sudoers file:
        #
        #     deploy ALL=(ALL) NOPASSWD: /bin/systemctl reload UNIT_NAME
        #
        # See: https://toroid.org/sudoers-syntax
        check_call(["sudo", "systemctl", "reload", self.UNIT_NAME])
