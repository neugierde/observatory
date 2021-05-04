import pytest
import time
import datetime
import re
from datetime import timedelta
from unittest.mock import patch, Mock
from context import Poller, SiteConfig


@pytest.fixture
def stubbed_successful_get(*args, **kwargs):
    with patch('requests.get') as get_mock:
        get_mock.side_effect = lambda *_, **__: Mock(**{
            'text': 'content',
            'status_code': 200,
            'ok': True,
            'elapsed': timedelta(milliseconds=120)
        })
        yield get_mock


@pytest.fixture
def notifier_mock(mocker):
    yield mocker.Mock()


@pytest.fixture
def owner_mock(mocker):
    yield mocker.Mock()


@pytest.fixture
def poller(notifier_mock, owner_mock):
    poller = Poller.start(notifier=notifier_mock, owner=owner_mock)

    yield poller.proxy()

    poller.stop()


def test_poller(poller, notifier_mock, stubbed_successful_get):
    poller.check(SiteConfig(url='https://google.com')).get()
    notifier_mock.notify.assert_called_once

    arg = notifier_mock.notify.call_args.args[0]
    assert arg['uri'] == 'https://google.com'
    assert arg['status'] == 200
    assert arg['time'] == datetime.timedelta(microseconds=120000)
    assert isinstance(arg['timestamp'], float)
    assert arg['match_re'] is None


def test_poller_with_matching_content(poller, notifier_mock, stubbed_successful_get):
    poller.check(SiteConfig(url='https://google.com', re=re.compile('cont'))).get()
    notifier_mock.notify.assert_called_once

    arg = notifier_mock.notify.call_args.args[0]
    assert arg['uri'] == 'https://google.com'
    assert arg['status'] == 200
    assert arg['time'] == datetime.timedelta(microseconds=120000)
    assert isinstance(arg['timestamp'], float)
    assert arg['match_re'] is True

def test_poller_without_matching_content(poller, notifier_mock, stubbed_successful_get):
    poller.check(SiteConfig(url='https://google.com', re=re.compile('notfound'))).get()
    notifier_mock.notify.assert_called_once

    arg = notifier_mock.notify.call_args.args[0]
    assert arg['uri'] == 'https://google.com'
    assert arg['status'] == 200
    assert arg['time'] == datetime.timedelta(microseconds=120000)
    assert isinstance(arg['timestamp'], float)
    assert arg['match_re'] is False
