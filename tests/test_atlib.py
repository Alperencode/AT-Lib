from source.atlib import ATLIB
from unittest.mock import patch, call
import pytest


@pytest.fixture
def at():
    with patch('source.atlib.serial.Serial') as _:
        at = ATLIB('/dev/ttyUSB0')
    return at


def test_init():
    with patch('source.atlib.serial.Serial') as mock_serial:
        at = ATLIB('/dev/ttyUSB0')

    mock_serial.assert_called_with(
        port='/dev/ttyUSB0',
        timeout=15,
        baudrate=115200,
        stopbits=at.stopbits,
        parity=at.parity
    )


def test_send_at_null(at):
    assert at.send_at("") is None


@patch('builtins.print')
def test_send_at_outputs(mock_print, at):
    at.send_at("AT")
    at.send_at("AT+CMD")

    expected_calls = [
        call("\033[32m[OK] AT command sent\033[0m"),
        call("AT"),
        call("\033[32m[OK] AT command sent\033[0m"),
        call("AT+CMD"),
    ]

    assert mock_print.call_args_list == expected_calls


@patch('builtins.print')
def test_send_at_exception_handling(mock_print, at):
    # Set up the mock_print to raise a RuntimeError with the specified message
    error_message = "[ERROR] Couldn't send AT command"
    mock_print.side_effect = Exception(error_message)

    # Assertions
    with pytest.raises(Exception) as e:
        at.send_at("AT")

    assert str(e.value) == error_message


def test_get_port():
    assert ATLIB.get_port() != "/dev/ttyAMA0"
