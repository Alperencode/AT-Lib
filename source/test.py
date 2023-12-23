# Testing serial module tools and function
from serial.tools import list_ports
from .atlib import ATLIB


def test():
    print("== Testing comports == ")
    for port in list_ports.comports():
        print(port.product)

    print("== Testing get_port == ")
    print(ATLIB.get_port())
