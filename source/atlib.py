from .logger import logGreen, logRed, log
from serial import SerialException
import time
import serial


class ATLIB:
    __delay = 1
    __last_command = ""

    def __init__(self, port, timeout=15, baudrate=115200):
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_NONE

        self.serial = serial.Serial(
            port=port,
            timeout=timeout,
            baudrate=baudrate,
            stopbits=self.stopbits,
            parity=self.parity
        )

    def __open_serial(self):    # pragma: no cover
        if not self.serial.is_open:
            try:
                self.serial.open()
            except SerialException:
                raise SerialException("[ERROR] Couldn't read response")

    def send_at(self, at):
        if at is None or len(at) <= 0:
            logRed("[ERROR] Null command")
            return
        self.__open_serial()

        at = at + "\r\n"

        try:
            self.serial.write(at.encode())
            time.sleep(ATLIB.__delay)
            ATLIB.__last_command = at.strip()
            logGreen("[OK] AT command sent")
            log(at.strip())
        except SerialException:
            raise SerialException("[ERROR] Couldn't send AT command")

    def get_response(self):
        self.__open_serial()
        response = b''

        data = self.serial.in_waiting
        if data == 0:
            logRed("[ERROR] No data to read")
            return ''

        try:
            response = self.serial.read(data).decode('utf-8')
        except UnicodeDecodeError:
            msg = "[ERROR] Couldn't decode response"
            raise UnicodeDecodeError('utf-8', response, 0, len(response), msg)
        except SerialException:
            raise SerialException("[ERROR] Couldn't read response")

        if "OK" in response:
            logGreen("[OK] Response received")
            response = response.split("OK")[0].strip()
            if response == ATLIB.__last_command:
                return "OK"
            # Following if branch currently not working
            if ATLIB.__last_command in response:    # pragma: no cover
                response.replace(ATLIB.__last_command, "")
            return response
        elif "ERROR" in response:
            logRed("[OK] Response received as ERROR")
            return "ERROR"
        else:
            logRed("[ERROR] Unexpected AT response")
            return ''

    def send_and_get(self, command):
        log()
        self.send_at(command)
        return self.get_response()

    @staticmethod
    def get_port():
        from serial.tools import list_ports

        for port in list_ports.comports():
            if port.product is not None:
                return port.device
