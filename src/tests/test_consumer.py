import pytest

from unittest.mock import MagicMock, Mock

import checkweb.consumer
import checkweb.check_event


def test_handle_event_dict():
    # based on https://stackoverflow.com/questions/28850070/python-mocking-a-context-manager
    # and a lot of trial and error...
    pg_cursor_context_mock = Mock()
    cursor_mock = Mock()
    pg_cursor_context_mock.return_value.__enter__ = cursor_mock
    pg_cursor_context_mock.return_value.__exit__ = Mock()
    execute_mock = Mock()
    cursor_mock.return_value.execute = execute_mock

    checkweb.consumer.pg.postgres_cursor_context = pg_cursor_context_mock

    check_event = dict(
        timestamp=1,
        url='http://www.whatever.de/',
        response_time_seconds=1.2,
        status_code=1,
        found_regex_pattern=False,
        exception_message=None,
        version=1,
    )

    checkweb.consumer.handle_event_dict(check_event)

    assert execute_mock.call_count == 1
    assert 'found_regex_pattern' in execute_mock.call_args.args[0]
    assert isinstance(execute_mock.call_args.args[1], dict)
    assert execute_mock.call_args.args[1]['url'] == check_event['url']


def test_handle_event_dict_with_bad_event(capsys):
    # based on https://stackoverflow.com/questions/28850070/python-mocking-a-context-manager
    # and a lot of trial and error...
    pg_cursor_context_mock = Mock()
    checkweb.consumer.pg.postgres_cursor_context = pg_cursor_context_mock

    check_event = dict(
        timestamp=1,
        url='http://www.whatever.de/',
        response_time_seconds=1.2,
        status_code=-1,
        found_regex_pattern=False,
        exception_message=None,
        version=1,
    )

    checkweb.consumer.handle_event_dict(check_event)
    captured = capsys.readouterr()
    assert 'ignoring event:' in captured.out
    assert pg_cursor_context_mock.call_count == 0


def test_migrate():
    pg_cursor_context_mock = Mock()
    cursor_mock = Mock()
    pg_cursor_context_mock.return_value.__enter__ = cursor_mock
    pg_cursor_context_mock.return_value.__exit__ = Mock()
    execute_mock = Mock()
    cursor_mock.return_value.execute = execute_mock
    checkweb.consumer.pg.postgres_cursor_context = pg_cursor_context_mock

    checkweb.consumer.migrate_db()

    # the last migration, so needs adjustments with every new one
    assert execute_mock.call_count == 2
    assert 'IF NOT EXISTS version SMALLINT NOT NULL DEFAULT 0' in execute_mock.call_args.args[0]

def test_main():
    checkweb.consumer.KafkaConsumer = MagicMock()
    kafka_consumer_instance = checkweb.consumer.KafkaConsumer.return_value
    event2_mock = MagicMock()
    event2_mock.value = {3,4}
    kafka_consumer_instance.__iter__.return_value = [MagicMock(), event2_mock]
    checkweb.consumer.migrate_db = MagicMock()
    checkweb.consumer.handle_event_dict = MagicMock()

    checkweb.consumer.main()

    assert checkweb.consumer.migrate_db.call_count == 1
    assert checkweb.consumer.KafkaConsumer.call_count == 1
    assert checkweb.consumer.handle_event_dict.call_count == 2
    assert checkweb.consumer.handle_event_dict.call_args.args[0] == event2_mock.value
