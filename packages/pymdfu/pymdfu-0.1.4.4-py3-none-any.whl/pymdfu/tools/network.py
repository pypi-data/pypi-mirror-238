import argparse
from ..mac import MacSocketClient
from ..uart_transport import UartTransport

_parser = argparse.ArgumentParser()
_parser.add_argument("--protocol",
    type=str,
    help="Protocol for network layer",
    choices=["serial"]
)
_parser.add_argument("--port",
    type=int,
    help="Port",
)
_parser.add_argument("--host",
    type=str,
    help="Host e.g. localhost, 127.0.0.1",
    default="localhost"
)

def tool_get_help():
    txt = _parser.format_help()
    return txt

def get_transport(arguments):
    args = _parser.parse_args(arguments)
    mac = MacSocketClient(args.port, args.host)
    transport = UartTransport(mac=mac)
    return transport


if __name__ == "__main__":
    txt = tool_get_help()
    print(txt)