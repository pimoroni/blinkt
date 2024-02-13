import sys

import mock
import pytest


@pytest.fixture(scope='function', autouse=True)
def cleanup():
    yield
    del sys.modules['blinkt']


@pytest.fixture(scope='function', autouse=False)
def gpiod():
    sys.modules['gpiod'] = mock.Mock()
    sys.modules['gpiod.line'] = mock.Mock()
    yield sys.modules['gpiod']
    del sys.modules['gpiod.line']
    del sys.modules['gpiod']


@pytest.fixture(scope='function', autouse=False)
def gpiodevice():
    sys.modules['gpiodevice'] = mock.Mock()
    yield sys.modules['gpiodevice']
    del sys.modules['gpiodevice']


@pytest.fixture(scope='function', autouse=False)
def gpiod_request():
    yield mock.MagicMock()
