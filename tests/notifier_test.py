import pytest
from context import Notifier


@pytest.fixture
def producer_mock(mocker):
    """
    Mocks a KafkaProducer.
    """
    yield mocker.Mock()


@pytest.fixture
def notifier(producer_mock):
    notifier = Notifier.start(producer=producer_mock, owner=None)

    yield notifier.proxy()

    notifier.stop()


def test_notifier(notifier, producer_mock):
    notifier.notify({'data': 'foo', 'other_data': 'bar'}).get()

    producer_mock.assert_called_once_with({'data': 'foo', 'other_data': 'bar'})
