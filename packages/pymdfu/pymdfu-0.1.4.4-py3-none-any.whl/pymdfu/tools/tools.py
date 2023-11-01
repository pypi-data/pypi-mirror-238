"""Tools manager for bootloader host application
"""
from pathlib import Path
from logging import getLogger
from . import nedbg
from . import serial_generic as serial
from . import mcp2221a
from . import network

supported_tools = [ 'serial', 'simulator', 'network']
logger = getLogger()

def parse_tools():
    """Look for tool implementation in package tools folder

    TODO Just an example for now. We might rather hardcode tools support instead of making this dynamic
    Assumes each tool is contained within one Python file.
    Ignores __init__.py and tools.py
    """
    tools_modules_path = Path(__file__).parent
    import importlib.util
    import sys
    tools = []
    for path in tools_modules_path.iterdir():
        if path.is_file() and not path.match("__init__.py") and not path.match("tools.py"):
            module_name = "pymdfu.tools." + path.name.rstrip(".py")
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            tools.append(module)
            logger.info("Found tool %s", path)
    # Example for how to iterate over dynamically loaded tools
    # for tool in tools:
        #print(tool.tool_get_help())

def list_supported_tools(args):
    """List supported tools"""
    print("Not implemented yet")

def list_connected_tools(args):
    """List connected tools"""
    serial_generic.list_connected()
    print("Other tools lookup not implemented yet")

def create_tools_help():
    """Create help for supported tools

    :return: Help description for supported tools
    :rtype: str
    """
    tools_help = ""
    for tool in supported_tools:
        tools_help += tool + "\n"
    return tools_help

def get_tool(tool, interface=None, tool_args=None):
    """Tools factory

    Returns a tool based on tool name and interface

    :param tool: Tool name
    :type tool: str
    :param interface: Tool interface e.g. UART, I2C etc., defaults to None
    :type interface: str, optional
    :param tool_args: Tool specific parameters, defaults to None
    :type tool_args: dict, optional
    :return: Tool object
    :rtype: Object inherited from Transport class
    """
    if tool not in supported_tools:
        raise ValueError(f'Tool "{tool}" is not in supported tools list {supported_tools} ')
    if tool == 'nedbg' and interface in ["uart", None]:
        transport = nedbg.get_transport(tool_args)
    elif tool == "serial":
        transport = serial.get_transport(tool_args)
    elif tool == "mcp2221a":
        if interface in {"uart", None}:
            transport = mcp2221a.get_transport(tool_args)
    elif tool == "network":
        transport = network.get_transport(tool_args)
    return transport

parse_tools()
