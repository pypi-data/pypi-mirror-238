"""
Contains helpers for interacting with Skyramp endpoints.
"""
from skyramp.test_pattern import _TestPattern as TestPattern
class _Test:
    """
    Base class for test description. This should not be used for instantiation.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=line-too-long
    def __init__(self, name: str, test_pattern: TestPattern, input_file: str, target: str, timeout: str, output_file: str, global_vars: map, global_headers: map ) -> None:
        self.name = name
        self.test_pattern = test_pattern
        self.input_file = input_file
        self.target = target
        self.timeout = timeout
        self.output_file = output_file
        self.global_vars = global_vars
        self.global_headers = global_headers


    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        return {
            "name": self.name,
            "testPattern": TestPattern.to_json(self.test_pattern),
            "inputFile": self.input_file,
            "target": self.target,
            "timeout": self.timeout,
            "outputFile": self.output_file,
            "globalVars": self.global_vars,
            "globalHeaders": self.global_headers,
        }
    