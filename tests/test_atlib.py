from source.atlib import ATLIB
import pytest


@pytest.fixture
def atlib():
    return ATLIB(
        port="/dev/ttyUSB3",
        baudrate=15200,
        timeout=10
    )


def test_init():
    atlib = ATLIB('/dev/ttyUSB3')
    assert atlib.serial.port == '/dev/ttyUSB3'
    assert atlib.serial.timeout == 15
    assert atlib.serial.baudrate == 115200
    assert atlib.serial.stopbits == atlib.stopbits
    assert atlib.serial.parity == atlib.parity


def test_get_port():
    assert ATLIB.get_port() != "/dev/ttyAMA0"
