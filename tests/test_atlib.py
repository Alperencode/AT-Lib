from source.atlib import ATLIB
from unittest.mock import patch
import pytest


@pytest.fixture
def atlib():
    return ATLIB(
        port="/dev/ttyUSB3",
        baudrate=15200,
        timeout=10
    )


def test_init():
    with patch('source.atlib.serial.Serial') as mock_serial:
        atlib = ATLIB('/dev/ttyUSB0')

    mock_serial.assert_called_with(
        port='/dev/ttyUSB0',
        timeout=15,
        baudrate=115200,
        stopbits=atlib.stopbits,
        parity=atlib.parity
    )


def test_get_port():
    assert ATLIB.get_port() != "/dev/ttyAMA0"
