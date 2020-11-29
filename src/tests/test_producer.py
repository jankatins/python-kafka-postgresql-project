import pytest
import httpx
import re

from unittest.mock import MagicMock

import checkweb.producer
import checkweb.check_event


def test_check_website_successful(httpx_mock):
    url = 'http://www.google.com.doesnotexist'
    pattern = 'google'
    httpx_mock.add_response(data=f"blablablkdsflkjdsf {pattern} kjgdsfk kjsadksajfg")

    event = checkweb.producer.check_website(url, re.compile(pattern))

    assert isinstance(event, checkweb.check_event.CheckEvent)
    assert event.url == url
    assert event.status_code == 200
    assert event.found_regex_pattern
    assert event.response_time_seconds > 0


def test_check_website_pattern_not_found(httpx_mock):
    url = 'http://www.google.com.doesnotexist'
    pattern = 'google'
    httpx_mock.add_response(data=f"blablablkdsflkjdsf kjgdsfk kjsadksajfg")

    event = checkweb.producer.check_website(url, re.compile(pattern))

    assert isinstance(event, checkweb.check_event.CheckEvent)
    assert event.url == url
    assert event.status_code == 200
    assert not event.found_regex_pattern
    assert event.response_time_seconds > 0

def test_check_website_no_regex_given(httpx_mock):
    url = 'http://www.google.com.doesnotexist'
    httpx_mock.add_response(data=f"blablablkdsflkjdsf kjgdsfk kjsadksajfg")

    event = checkweb.producer.check_website(url, None)

    assert isinstance(event, checkweb.check_event.CheckEvent)
    assert event.url == url
    assert event.status_code == 200
    assert event.found_regex_pattern is None
    assert event.response_time_seconds > 0


def test_check_website_404(httpx_mock):
    url = 'http://www.google.com.doesnotexist'
    pattern = 'google'
    httpx_mock.add_response(status_code=404, data=f"")

    event = checkweb.producer.check_website(url, re.compile(pattern))

    assert isinstance(event, checkweb.check_event.CheckEvent)
    assert event.url == url
    assert event.status_code == 404
    assert not event.found_regex_pattern
    assert event.response_time_seconds > 0


def test_check_website_timeout(httpx_mock):
    url = 'http://www.google.com.doesnotexist'
    pattern = 'google'
    # no respond => httpx.TimeoutException is raised

    event = checkweb.producer.check_website(url, re.compile(pattern))

    assert isinstance(event, checkweb.check_event.CheckEvent)
    assert event.url == url
    assert event.status_code is None
    assert event.found_regex_pattern is None
    assert event.response_time_seconds > 0


# Mock docs: https://docs.python.org/3/library/unittest.mock.html

@pytest.mark.parametrize('count,pattern', [(1, 'google'), (2, None)])
def test_run_producer(httpx_mock, count, pattern):
    url = 'http://www.google.com.doesnotexist'
    httpx_mock.add_response(status_code=404, data=f"")

    mock_kafka_producer = MagicMock()

    checkweb.producer.run_producer(kafka_producer=mock_kafka_producer,
                              kafka_topic='test_topic',
                              max_loops=count,
                              wait_between_scrapes=0,
                              url=url,
                              regex=re.compile(pattern) if pattern else None)

    assert mock_kafka_producer.send.call_count == count
    assert mock_kafka_producer.send.call_args.args[0] == 'test_topic'
    assert mock_kafka_producer.send.call_args.kwargs['value']['url'] == url


def test_main():
    kafka_producer_class_mock = MagicMock()
    checkweb.producer.KafkaProducer = kafka_producer_class_mock

    run_producer_mock = MagicMock()
    checkweb.producer.run_producer = run_producer_mock

    checkweb.producer.main()

    # creates a KafkaProducer
    assert kafka_producer_class_mock.call_count == 1

    # runs the loop
    assert run_producer_mock.call_count == 1
