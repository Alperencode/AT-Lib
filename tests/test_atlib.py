from source.atlib import ATLIB
from unittest.mock import patch, call, MagicMock
from serial import SerialException
import pytest
import re


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
    assert at.send_at('') is None
    assert at.send_at(None) is None


def test_send_at_exception_handling(at):
    at.serial = MagicMock()
    error_msg = "[ERROR] Couldn't send AT command"

    with patch.object(at.serial, 'write', side_effect=SerialException):
        with pytest.raises(SerialException, match=re.escape(error_msg)):
            at.send_at("example_command")


def test_get_response_unicode_exception(at):
    # Mocking serial object and setting up expectations
    at.serial = MagicMock()
    at.serial.in_waiting = 8
    at.serial.read.return_value = b'\x80\x81\x82'  # Invalid UTF-8 sequence

    error_msg = "[ERROR] Couldn't decode response"
    with pytest.raises(UnicodeDecodeError, match=re.escape(error_msg)):
        at.get_response()


def test_get_response_serial_exception(at):
    at.serial = MagicMock()
    error_msg = "[ERROR] Couldn't read response"

    with patch.object(at.serial, 'read', side_effect=SerialException):
        with pytest.raises(SerialException, match=re.escape(error_msg)):
            at.get_response()


@patch('builtins.print')
def test_get_response_no_data(mock_print, at):
    at.serial.in_waiting = 0
    assert at.get_response() == ''

    expected_calls = [
        call("\033[31m[ERROR] No data to read\033[0m"),
    ]

    assert mock_print.call_args_list == expected_calls


@patch('builtins.print')
def test_get_response(mock_print, at):
    at.serial = MagicMock()
    at.serial.read.return_value = b'\nOK\nAT\n'
    assert at.get_response() == "OK"

    at.serial.read.return_value = b'\nAT+CSQ\n+CSQ: 18,99\nOK\n'
    assert at.get_response() == "AT+CSQ\n+CSQ: 18,99"

    at.serial.read.return_value = b'Random Response'
    assert at.get_response() == ''

    expected_calls = [
        call("\033[32m[OK] Response received\033[0m"),
        call("\033[32m[OK] Response received\033[0m"),
        call("\033[31m[ERROR] Unexpected AT response\033[0m"),
    ]

    assert mock_print.call_args_list == expected_calls


@patch('builtins.print')
def test_get_response_error(mock_print, at):
    at.serial = MagicMock()
    at.serial.read.return_value = b'\nAT?\nERROR\n'
    assert at.get_response() == "\nAT?\nERROR\n"

    at.serial.read.return_value = b'\nATE3\nERROR\n'
    assert at.get_response() == "\nATE3\nERROR\n"

    expected_calls = [
        call("\033[31m[OK] Response received as ERROR\033[0m"),
        call("\033[31m[OK] Response received as ERROR\033[0m"),
    ]

    assert mock_print.call_args_list == expected_calls


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
def test_send_and_get(mock_print, at):
    at.serial.read.return_value = b'\nAT+CMEE=2\nOK\n'
    response = at.send_and_get("AT+CMEE=2")
    assert response == "OK"

    expected_calls = [
        call(""),
        call("\033[32m[OK] AT command sent\033[0m"),
        call("AT+CMEE=2"),
        call("\033[32m[OK] Response received\033[0m"),
    ]

    assert mock_print.call_args_list == expected_calls
