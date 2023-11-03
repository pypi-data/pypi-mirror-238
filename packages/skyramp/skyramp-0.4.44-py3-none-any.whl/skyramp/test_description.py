"""
Contains helpers for interacting with Skyramp endpoints.
"""

from skyramp.test import _Test as Test
from skyramp.test_command import _TestCommand as TestCommand
from skyramp.test_request import _Request as Request
from skyramp.scenario import _Scenario as Scenario
from skyramp.service import _Service as Service
from skyramp.endpoint import _Endpoint as Endpoint

class _TestDescription:
    """
    Base class for test description. This should not be used for instantiation.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=line-too-long
    def __init__(self, version: str, test: Test, scenarios: [Scenario], requests: [Request], commands: [TestCommand], endpoints: [Endpoint],  services: [Service] ) -> None:
        self.version = version
        self.test = test
        self.scenarios = scenarios
        self.requests = requests
        self.commands = commands
        self.endpoints = endpoints
        self.services = services


    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        return {
            "version": self.version,
            "test": Test.to_json(self.test),
            "scenarios": self.scenarios,
            "requests": Request.as_request_dict(self.requests),
            "commands": TestCommand.to_json(self.commands),
            "services": Service.to_json(self.services),
            "endpoints": self.endpoints,
        }
    