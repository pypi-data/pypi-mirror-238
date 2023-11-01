"""Command line interface for MDFU client"""
import logging
import os
import sys
import argparse
import textwrap
import time
from logging.config import dictConfig
from appdirs import user_log_dir
import yaml
from yaml.scanner import ScannerError
from .pymdfuclient import MdfuClient
from .mac import MacFactory
from .uart_transport import UartTransport

try:
    from . import __version__ as VERSION
    from . import BUILD_DATE, COMMIT_ID
except ImportError:
    print("Version info not found!")
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

def run_mdfu_client(port, host, transport_protocol="serial"):
    """Run MDFU client

    Terminate the client with CTRL-C

    :param port: Port
    :type port: int
    :param host: Host e.g. 127.0.0.1, localhost
    :type host: str
    :param transport_protocol: Transport protocol to use, defaults to "serial"
    :type transport_protocol: str, optional
    """
    mac = MacFactory.get_socket_host_mac(host, port)
    if transport_protocol == "serial":
        transport = UartTransport(mac)
    client = MdfuClient(transport)
    client.start()
    try:
        while client.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        client.stop()

def setup_logging(user_requested_level=logging.WARNING, default_path='logging.yaml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI
    """
    # Logging config YAML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the YAML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rt', encoding="UTF-8") as file:
                # Load logging configfile from yaml
                configfile = yaml.safe_load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    os.makedirs(logdir, exist_ok=True)

                if user_requested_level <= logging.DEBUG:
                    # Using a different handler for DEBUG level logging to be able to have a more detailed formatter
                    configfile['root']['handlers'].append('console_detailed')
                    # Remove the original console handlers
                    try:
                        configfile['root']['handlers'].remove('console_only_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                    try:
                        configfile['root']['handlers'].remove('console_not_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                else:
                    # Console logging takes granularity argument from CLI user
                    configfile['handlers']['console_only_info']['level'] = user_requested_level
                    configfile['handlers']['console_not_info']['level'] = user_requested_level

                # Root logger must be the most verbose of the ALL YAML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except ScannerError:
            # Error while parsing YAML
            print(f"Error parsing logging config file '{path}'")
        except KeyError as keyerror:
            # Error looking for custom fields in YAML
            print(f"Key {keyerror} not found in logging config file")
    else:
        # Config specified by environment variable not found
        print(f"Unable to open logging config file '{path}'")

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

def main():
    """
    Entrypoint for installable CLI

    Configures the CLI and parses the arguments
    """
    # Shared switches.  These are inherited by subcommands (and root) using parents=[]
    common_argument_parser = argparse.ArgumentParser(add_help=False)
    common_argument_parser.add_argument("-v", "--verbose",
                                        default="info",
                                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                                        help="Logging verbosity/severity level")

    parser = argparse.ArgumentParser(
        parents=[common_argument_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent('''\
    pymdfuclient: Microchip Device Firmware Upgrade client

    basic usage:
        - pymdfuclient <port> <host> [-switches]
            '''),
        epilog=textwrap.dedent('''usage examples:
    Start client on localhost port 5558
                               
    - pymdfuclient 5558 localhost

    '''))

    # Action-less switches.  These are all "do X and exit"
    parser.add_argument("-V", "--version", action="store_true",
                        help="Print pymdfuclient version number and exit")
    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print pymdfuclient release details and exit")

    parser.add_argument("--protocol",
            type=str,
            help="Protocol for network layer",
            choices=["serial"]
    )
    parser.add_argument("port",
            type=int,
            help="Port",
            default="5559",
            nargs='?'
    )
    parser.add_argument("host",
            type=str,
            help="Host e.g. localhost, 127.0.0.1",
            default="localhost",
            nargs='?'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))
    logger = logging.getLogger(__name__)

    if args.version or args.release_info:
        print(f"pymdfuclient version {VERSION}")
        if args.release_info:
            print(f"Build date:  {BUILD_DATE}")
            print(f"Commit ID:   {COMMIT_ID}")
            print(f"Installed in {os.path.abspath(os.path.dirname(__file__))}")
        return 0

    try:
        run_mdfu_client(args.port, args.host)
    # pylint: disable-next=broad-exception-caught
    except Exception as exc:
        logger.error("Operation failed with %s: %s", type(exc).__name__, exc)
        if args.verbose != "debug":
            logger.error("For more information run with -v debug")
        logger.debug(exc, exc_info=True)    # get traceback if debug loglevel
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
