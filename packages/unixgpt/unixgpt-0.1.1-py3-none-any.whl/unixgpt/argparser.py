import argparse

from .constants import VERSION


def parse():
    parser = argparse.ArgumentParser(
        prog="unixgpt",
        description="Bridges the gap between natural language and UNIX commands"
    )

    # collect input (required)
    parser.add_argument(
        "-i", "--input",
        type=str,
        help="Natural language input to be converted to unix command. Enclose in quotation marks."
    )

    # show saved commands in unixgpt local library
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List saved commands in UnixGPT local library"
    )

    # save command to unixgpt local library
    parser.add_argument(
        "-s", "--save",
        type=str,
        help="Store a command in UnixGPT local library for easy access"
    )

    # fetch a command from unixgpt local library with natural language or by ID
    parser.add_argument(
        "-f", "--fetch",
        type=str,
        help="Fetch a command from UnixGPT local library with natural language or by ID"
    )

    # delete a saved command from unixgpt local library by ID
    parser.add_argument(
        "-d", "--delete",
        type=str,
        help="Delete a saved command from UnixGPT local library"
    )

    # unixgpt version
    parser.add_argument(
        "--version",
        action="version",
        version=VERSION,
        help="Print version information and quit"
    )
    
    args = parser.parse_args()
    return args
