"""Serial port tool
"""
import argparse
from ..utils import si_postfix_unit_to_int
from ..mac import MacFactory
from ..uart_transport import UartTransport
import serial.tools.list_ports

parser = argparse.ArgumentParser()
parser.add_argument("--baudrate",
    type=si_postfix_unit_to_int,
    help="Baudrate",
    required=True
)
parser.add_argument("--port",
    type=str,
    help="Serial port e.g. COM1 on Windows or /dev/ttyACM0 on Linux",
    required=True
)

def tool_get_help():
    txt = parser.format_help()
    return txt

def get_transport(arguments):
    args = parser.parse_args(arguments)
    mac = MacFactory.get_serial_port_mac(args.port, args.baudrate)
    transport = UartTransport(mac=mac)
    return transport

def list_connected():
    comports = serial.tools.list_ports.comports()
    print(f"Found serial ports:")
    for port in comports:
        print(f"{port}", end=None)
    print("")
    # usbports = [p for p in comports if "USB" in p.hwid]
    # print(f"\nFound usbports:")
    # for port in usbports:
    #     print(f"{port}", end=None)
    # print("")
