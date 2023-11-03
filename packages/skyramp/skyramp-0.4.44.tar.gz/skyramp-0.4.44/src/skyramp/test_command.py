"""
Contains helpers for interacting with Skyramp endpoints.
"""

class _TestCommand:
    """
    Base class for test command. This should not be used for instantiation.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, name: str, command, dir_, asserts) -> None:
        self.name = name
        self.command = command
        self.dir_ = dir_
        self.asserts = asserts

        self.test_command = {
            "name": self.name,
            "command": self.command,
            "dir_": self.dir_,
            "asserts": self.asserts,
        }

    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        return {
            "name": self.name,
            "command": self.command,
            "dir": self.dir_,
            "asserts": self.asserts,
        }
    