import pytest

from app.check_event import CheckEvent

def test_serialisation():
    e = CheckEvent(timestamp=1,
                   url='',
                   response_time_seconds=1.2,
                   status_code=1,
                   found_regex_pattern=False,
                   exception_message=None,
                   version=1)
    assert e == CheckEvent.from_dict(e.to_dict())
