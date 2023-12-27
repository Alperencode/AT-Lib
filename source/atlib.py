from .logger import logGreen, logRed, log
from serial import SerialException
import time
import serial


class ATLIB:
    __delay = 1
    __last_command = ""

    def __init__(self, port, timeout=15, baudrate=115200):
        """
        Initializes serial object with given port and configurations
        """
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_NONE

        # Initialize serial object
        self.serial = serial.Serial(
            port=port,
            timeout=timeout,
            baudrate=baudrate,
            stopbits=self.stopbits,
            parity=self.parity
        )

    def __open_serial(self):    # pragma: no cover
        """
        Finds valid port for serial communication
        """
        if not self.serial.is_open:
            try:
                self.serial.open()
            except SerialException:
                raise SerialException("[ERROR] Couldn't read response")

    def send_at(self, at):
        """
        Sends given command to serial port
        """
        # If no command given, return
        if at is None or len(at) <= 0:
            logRed("[ERROR] Null command")
            return
        self.__open_serial()

        # Add ending flags to message
        at = at + "\r\n"

        try:
            # Encode and write message
            self.serial.write(at.encode())

            # Delay message for reading process
            time.sleep(ATLIB.__delay)

            # Set last command as given
            ATLIB.__last_command = at.strip()

            # Log results
            logGreen("[OK] AT command sent")
            log(at.strip())
        except SerialException:
            raise SerialException("[ERROR] Couldn't send AT command")

    def get_response(self):
        """
        Reads serial port buffer for response
        Returns decoded data
        """
        self.__open_serial()
        response = b''

        # Check buffer if there is any data to read
        data = self.serial.in_waiting
        if data == 0:
            logRed("[ERROR] No data to read")
            return ''

        try:
            # Read buffer using data size
            response = self.serial.read(data).decode('utf-8')
        except UnicodeDecodeError:
            # Handle decoding error
            msg = "[ERROR] Couldn't decode response"
            raise UnicodeDecodeError('utf-8', response, 0, len(response), msg)
        except SerialException:
            raise SerialException("[ERROR] Couldn't read response")

        if "OK" in response:
            # Log response status
            logGreen("[OK] Response received")

            # Select the first string
            response = response.split("OK")[0].strip()

            # Compare string with last command
            if response == ATLIB.__last_command:
                # If same, return "OK" (Example: "AT" -> "OK")
                # Implemented to prevent printing commands repeatedly
                return "OK"

            # Otherwise, return pure response
            return response
        elif "ERROR" in response:
            # Log error
            logRed("[OK] Response received as ERROR")
            return response
        else:
            logRed("[ERROR] Unexpected AT response")
            return ''

    def send_and_get(self, command):
        """
        Sends AT command and returns received response
        """
        log()
        self.send_at(command)
        return self.get_response()

    @staticmethod
    def get_port():     # pragma: no cover
        """
        Finds valid port for serial communication
        """
        from serial.tools import list_ports

        # Iterate comports
        for port in list_ports.comports():
            # If product is not null, select port
            if port.product is not None:
                return port.device
        return None
