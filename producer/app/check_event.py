"""The CheckEvent

This file is defined at the producer and automatically copied to the consumer by the makefile.
Only edit at the producer side!

->  Poor man's substitution for a schema definition in a central place...
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
