import sys

import mock
import pytest


@pytest.fixture(scope='function', autouse=False)
def gpiod():
    sys.modules['gpiod'] = mock.Mock()
    sys.modules['gpiod.line'] = mock.Mock()
    yield sys.modules['gpiod']
    del sys.modules['gpiod.line']
    del sys.modules['gpiod']