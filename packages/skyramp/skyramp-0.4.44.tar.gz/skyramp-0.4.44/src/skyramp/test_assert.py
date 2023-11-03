"""
Contains helpers for interacting with Skyramp testing scenarios.
"""
# pylint: disable=too-few-public-methods
class _Assert:
    def __init__(self, assert_value: str, assert_expected_value: str) -> None:
        self.assert_value = assert_value
        self.assert_expected_value = assert_expected_value

    def as_step_dict(self):
        """
        Convert the object to a JSON string.
        """
        assert_string = f'requests.{self.assert_value} == "{self.assert_expected_value}"'
        return {
            "asserts": assert_string 
        }
    