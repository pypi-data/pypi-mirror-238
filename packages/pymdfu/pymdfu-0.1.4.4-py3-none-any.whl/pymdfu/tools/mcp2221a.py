"""MCP2221A tool"""
import argparse
from ..utils import si_postfix_unit_to_int
from ..mac import MacFactory
from ..uart_transport import UartTransport

_parser = argparse.ArgumentParser()

_parser.add_argument("--baudrate",
    type=si_postfix_unit_to_int,
    help="Baudrate",
    required=True
)
_parser.add_argument("--port",
    type=str,
    help="Serial port e.g. COM1 on Windows or /dev/ttyACM0 on Linux",
    required=True
)

def tool_get_help():
    txt = _parser.format_help()
    return txt

def get_transport(arguments):
    args = _parser.parse_args(arguments)
    mac = MacFactory.get_serial_port_mac(args.port, args.baudrate)
    transport = UartTransport(mac=mac)
    return transport
