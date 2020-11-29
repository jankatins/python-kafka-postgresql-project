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


def test_from_dict_creation_from_v0():
    e = dict(timestamp=1,
             url='http://www.whatever.de/',
             response_time_seconds=1.2,
             status_code=1,
             found_regex_pattern=False)
    assert CheckEvent.from_dict(e).version == 0


@pytest.mark.parametrize('bad_content,msg', [
    ({'exception_message': 'set'}, 'exception_message'),
    ({'status_code': -1}, 'status_code'),
    ({'response_time_seconds': -1.2}, 'response_time_seconds'),
    ({'url': None}, 'url'),
    ({'version': 99}, 'url'),
])
def test_from_dict_creation_from_bad_events(bad_content, msg):
    # create a good dict and then change it to a bad one
    event = CheckEvent(timestamp=1,
                       url='http://www.whatever.de/',
                       response_time_seconds=1.2,
                       status_code=200,
                       found_regex_pattern=True,
                       exception_message=None,
                       version=1).to_dict()

    event.update(bad_content)

    with pytest.raises(RuntimeError, match=msg):
        CheckEvent.from_dict(event)

@pytest.mark.parametrize('good_content', [
    ({'found_regex_pattern': None}),
])
def test_from_dict_creation_from_good_but_unnormal_events(good_content):
    event = CheckEvent(timestamp=1,
                       url='http://www.whatever.de/',
                       response_time_seconds=1.2,
                       status_code=200,
                       found_regex_pattern=True,
                       exception_message=None,
                       version=1).to_dict()

    event.update(good_content)

    CheckEvent.from_dict(event)
