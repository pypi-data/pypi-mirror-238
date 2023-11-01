"""
pymdfu CLI: "pymdfu"
"""
import sys
import logging
import argparse
import os
import textwrap

from logging.config import dictConfig
from appdirs import user_log_dir
import yaml
from yaml.scanner import ScannerError

from .status_codes import STATUS_SUCCESS
from .tools.tools import list_connected_tools, list_supported_tools, create_tools_help, supported_tools, get_tool
from .mdfu import Mdfu, MdfuUpdateError

from .mac import MacFactory
from .uart_transport import UartTransport
from .pymdfuclient import MdfuClient

try:
    from . import __version__ as VERSION
    from . import BUILD_DATE, COMMIT_ID
except ImportError:
    print("Version info not found!")
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

def simulate_update(upgrade_image, arguments):
    """Simulate update

    :param upgrade_image: Firmware image
    :type upgrade_image: bytes like object
    """
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mac",
        type=str,
        help="Mac layer",
        choices=["socketpair", "bytes", "packet"],
        default="bytes"
    )
    parser.add_argument("--port",
        type=int,
        help="Port",
    )
    parser.add_argument("--host",
        type=str,
        help="Host e.g. localhost, 127.0.0.1",
    )
    args = parser.parse_args(arguments)
    if args.mac == "bytes":
        mac_host, mac_client = MacFactory.get_bytes_based_mac()
    elif args.mac == "socketpair":
        mac_host, mac_client = MacFactory.get_socketpair_based_mac()
    elif args.mac == "packet":
        mac_host, mac_client = MacFactory.get_packet_based_mac()

    transport_client = UartTransport(mac=mac_client, timeout=1)
    client = MdfuClient(transport_client)

    transport_host = UartTransport(mac=mac_host, timeout=5)
    host = Mdfu(transport_host)

    client.start()
    try:
        host.run_upgrade(upgrade_image)
        logger.info("Simulated upgrade finished successfully")
    except MdfuUpdateError:
        logger.error("Simulated upgrade failed")
    client.stop()

def update(args):
    """Perform firmware update

    :param args: Arguments from command line
    :type args: dict
    """
    logger = logging.getLogger(__name__)
    with open(args.image, "rb") as file:
        image = file.read()
        if args.tool in ["simulator", "--simulator"]:
            simulate_update(image, args.tool_args)
        else:
            tool = get_tool(args.tool, tool_args=args.tool_args)
            mdfu = Mdfu(tool)
            try:
                mdfu.run_upgrade(image)
                logger.info("Upgrade finished successfully")
            except MdfuUpdateError:
                logger.error("Upgrade failed")

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
    pymdfu: a command line interface for Microchip bootloaders

    basic usage:
        - pymdfu <action> <tool> [-switches]
            '''),
        epilog=textwrap.dedent('''usage example:
    Update firmware through serial port and with update_image.img
    - pymdfu update serial update_image.img

    '''))


    # Action-less switches.  These are all "do X and exit"
    parser.add_argument("-V", "--version", action="store_true",
                        help="Print pymdfu version number and exit")
    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print pymdfu release details and exit")

    # First 'argument' is the command, which is a sub-parser
    subparsers = parser.add_subparsers(title='commands',
                                       dest='command',
                                       description="use one and only one of these commands",
                                       help="for additional help use pymdfu <command> --help")
    # Make the command required but not for -V or -R arguments
    subparsers.required = not any(arg in ["-V", "--version", "-R", "--release-info"] for arg in sys.argv)

    # These commands will be re-introduced after 0.1beta release
    # # List connected tools command
    # list_connected_tools_cmd = subparsers.add_parser(name='list',
    #                                           formatter_class=argparse.RawTextHelpFormatter,
    #                                           help='List connected tools',
    #                                           parents=[common_argument_parser])

    # # Configure the command handler for listing connected tools
    # list_connected_tools_cmd.set_defaults(func=list_connected_tools)

    # list_connected_tools_cmd = subparsers.add_parser(name='list-supported',
    #                                           formatter_class=argparse.RawTextHelpFormatter,
    #                                           help='List supported tools',
    #                                           parents=[common_argument_parser])
    # list_connected_tools_cmd.set_defaults(func=list_supported_tools)

    update_cmd = subparsers.add_parser(name='update',
                                       formatter_class=argparse.RawTextHelpFormatter,
                                       help='Update firmware',
                                       parents=[common_argument_parser])
    update_cmd.set_defaults(func=update)

    update_cmd.add_argument("tool",
                            choices=supported_tools,
                            help=create_tools_help())
    update_cmd.add_argument("image", type=str, help="Firmware upgrade image file")

    update_cmd.add_argument("tool_args", nargs=argparse.REMAINDER)

    # Parse
    args = parser.parse_args()

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))

    # Dispatch
    if args.version or args.release_info:
        print(f"pymdfu version {VERSION}")
        if args.release_info:
            print(f"Build date:  {BUILD_DATE}")
            print(f"Commit ID:   {COMMIT_ID}")
            print(f"Installed in {os.path.abspath(os.path.dirname(__file__))}")
        return STATUS_SUCCESS

    # Call the command handler
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
