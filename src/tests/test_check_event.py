import pytest

from checkweb.check_event import CheckEvent

def test_serialisation():
    e = CheckEvent(timestamp=1,
                   url='http://www.whatever.de/',
                   response_time_seconds=1.2,
                   status_code=1,
                   found_regex_pattern=False,
                   exception_message=None,
                   version=1)
    assert e == CheckEvent.from_dict(e.to_dict())

@pytest.mark.parametrize('bad_content,msg', [
    ({'exception_message': 'set'},'exception_message'),
    ({'status_code': -1},'status_code'),
    ({'response_time_seconds': -1.2},'response_time_seconds'),
    ({'url': None},'url'),
])
def test_bad_events(bad_content,msg):
    # create a good dict and then change it to a bad one
    event = CheckEvent(timestamp=1,
                   url='http://www.whatever.de/',
                   response_time_seconds=1.2,
                   status_code=200,
                   found_regex_pattern=True,
                   exception_message=None,
                   version=1).to_dict()

    event.update(bad_content)

    with pytest.raises(AssertionError, match=msg):
        CheckEvent.from_dict(event)
