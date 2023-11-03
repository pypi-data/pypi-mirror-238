"""
Contains helpers for interacting with Skyramp test pattern.
"""
class _TestPattern:
    """
    Base class for test pattern. This should not be used for instantiation.
    """
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=line-too-long
    def __init__(self, scenario_name: str, command: str, request_name: str, start_at, duration, at_once, ramp_up, steps, timeout, asserts, target_rps) -> None:

        self.scenario_name = scenario_name
        self.command =command
        self.request_name = request_name
        self.start_at = start_at
        self.duration = duration
        self.at_once = at_once
        self.ramp_up = ramp_up
        self.steps = steps
        self.timeout = timeout
        self.asserts = asserts
        self.target_rps = target_rps

        self.test_pattern = {
            "scenario_name": self.scenario_name,
            "command": self.command,
            "request_name": self.request_name,
            "start_at": self.start_at,
            "duration": self.duration,
            "at_once": self.at_once,
            "rampUp": self.ramp_up,
            "steps": self.steps,
            "timeout": self.timeout,
            "asserts": self.asserts,
            "target_rps": self.target_rps,
        }

    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        return {
            "scenarioName": self.scenario_name,
            "command": self.command,
            "requestName": self.request_name,
            "startAt": self.start_at,
            "duration": self.duration,
            "atOnce": self.at_once,
            "rampUp": self.ramp_up,
            "steps": self.steps,
            "timeout": self.timeout,
            "asserts": self.asserts,
            "targetRPS": self.target_rps,
        }
