import serial


class ATLIB:
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

    @staticmethod
    def get_port():
        from serial.tools import list_ports

        for port in list_ports.comports():
            if port.product is not None:
                return port.device
