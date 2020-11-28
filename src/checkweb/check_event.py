"""The CheckEvent

->  Poor man's replacement for a event schema definition ...
"""

import dataclasses
import typing as t


@dataclasses.dataclass()
class CheckEvent():
    timestamp: float
    url: str
    response_time_seconds: float
    status_code: int
    found_regex_pattern: bool
    exception_message: t.Optional[str] = None
    version: int = 1

    def __post_init__(self):
        # some validation, should probably raise a better exception
        if self.exception_message:
            msg = "If exception_message is set, status_code and found_regex_pattern must both be None"
            assert self.status_code is None and self.found_regex_pattern is None, msg
        assert self.response_time_seconds > 0, "response_time_seconds must be greater than 0"
        assert self.status_code is None or self.status_code > 0, "status_code must be None or an integer >0"
        assert self.url, "url must be set to a non-empty string"

    def to_dict(self):
        """Converts this CheckEvent instance to a dict"""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: dict):
        """Builds a CheckEvent from the dict"""
        version = d.get('version')
        if version == 1:
            return CheckEvent(**d)
        else:
            raise RuntimeError(f"Cannot build a CheckEvent from dict: {d}")
