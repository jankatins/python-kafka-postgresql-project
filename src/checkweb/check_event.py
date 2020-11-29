"""The CheckEvent

->  Poor man's replacement for a event schema definition ...
"""

import dataclasses
import typing as t
import datetime


@dataclasses.dataclass()
class CheckEvent():
    timestamp: float
    url: str
    response_time_seconds: float
    status_code: int
    found_regex_pattern: t.Optional[bool] = None
    exception_message: t.Optional[str] = None
    version: int = 1

    def __post_init__(self):
        # some validation, should probably raise a better exception
        if self.exception_message:
            msg = "If exception_message is set, status_code and found_regex_pattern must both be None"
            if not (self.status_code is None and self.found_regex_pattern is None):
                raise RuntimeError(msg)
        if not (self.response_time_seconds > 0):
            raise RuntimeError("response_time_seconds must be greater than 0")
        if not (self.status_code is None or self.status_code > 0):
            raise RuntimeError("status_code must be None or an integer >0")
        if not self.url:
            raise RuntimeError("url must be set to a non-empty string")

    def to_dict(self):
        """Converts this CheckEvent instance to a dict"""
        return dataclasses.asdict(self)

    def to_database_dict(self):
        """Converts to a dict which is suiteable to put into a DB

        Mainly converts the epoch timestamp to a real datetime with UTC timezone
        """
        db_dict = dataclasses.asdict(self)
        # always pass in a tz! https://blog.ganssle.io/articles/2019/11/utcnow.html
        db_dict['timestamp'] = datetime.datetime.fromtimestamp(self.timestamp, tz=datetime.timezone.utc)
        return db_dict

    @classmethod
    def from_dict(cls, d: dict):
        """Builds a CheckEvent from the dict"""
        version = d.get('version')
        if version is None:
            # initial versions of the event had no version nor a exception_message
            # we can ignore the exception_message case as the producer would error so also would not send such an event
            return CheckEvent(**d, version=0)
        elif version == 1:
            return CheckEvent(**d)
        else:
            raise RuntimeError(f"Cannot build a CheckEvent from dict: {d}")
