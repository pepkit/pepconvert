import sys
import jsonschema
import logging
import os
import yaml

from warnings import catch_warnings as cw

from logmuse import init_logger
from ubiquerg import VersionInHelpParser, size
from pkg_resources import iter_entry_points
from peppy import Project

from . import __version__

_LOGGER = logging.getLogger(__name__)

LOGGING_LEVEL="info"

_LEVEL_BY_VERBOSITY = [logging.ERROR, logging.CRITICAL, logging.WARN,
                       logging.INFO, logging.DEBUG]

PKG_NAME="pepconvert"


def build_argparser():
    banner = "%(prog)s - Interact with PEPs"
    additional_description = "\nhttp://eido.databio.org/"

    parser = VersionInHelpParser(
            prog=PKG_NAME,
            description=banner,
            epilog=additional_description,
            version=__version__)

    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument(
            "--verbosity", dest="verbosity",
            type=int, choices=range(len(_LEVEL_BY_VERBOSITY)),
            help="Choose level of verbosity (default: %(default)s)")
    parser.add_argument(
            "--logging-level", dest="logging_level",
            help="logging level")
    parser.add_argument(
            "--dbg", dest="dbg", action="store_true",
            help="Turn on debug mode (default: %(default)s)")
    sps = {}

    SUBPARSER_MSGS = {
        "convert": "Convert a PEP using an available filter",
        "list": "List available filters"
    }

    for cmd, desc in SUBPARSER_MSGS.items():
        sps[cmd] = subparsers.add_parser(cmd, description=desc, help=desc)

    sps["convert"].add_argument('pep', metavar="PEP",
                              help="Path to a PEP configuration "
                                   "file in yaml format.")

    sps["convert"].add_argument(
        "-f", "--format", required=True, default="yaml",
        help="Path to a PEP schema file in yaml format.")


    sps["convert"].add_argument(
        "-n", "--sample-name", required=False, nargs="+",
        help="Name of the samples to inspect.")

    return parser


def plugins():
    """
    Plugins registered by entry points in the current Python env

    :return dict[dict[function(refgenconf.RefGenConf)]]: dict which keys
        are names of all possible hooks and values are dicts mapping
        registered functions names to their values
    """
    return {ep.name: ep.load() for ep in iter_entry_points("pep.filters")}
    

def convert_project(prj, format):
    run_filter(prj, format)
    sys.exit(0)


def my_basic_plugin(p):
    print(p)

def complete_yaml(p):
    import re
    for s in p.samples:
        sys.stdout.write("- ")
        out = re.sub('\n', '\n  ', yaml.safe_dump(s.to_dict(), default_flow_style=False))
        sys.stdout.write(out + "\n")


def run_filter(prj, filter_name):
    myplugins = plugins()

    for name, func in myplugins.items():
        if name ==filter_name:
            _LOGGER.info(f"running plugin {name}")
            func(prj)


def list_formats():
    myplugins = plugins()

    for name, func in myplugins.items():
        _LOGGER.info(f"{name}")


def main():
    """ Primary workflow """
    parser = build_argparser()
    args, remaining_args = parser.parse_known_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    # Set the logging level.
    if args.dbg:
        # Debug mode takes precedence and will listen for all messages.
        level = args.logging_level or logging.DEBUG
    elif args.verbosity is not None:
        # Verbosity-framed specification trumps logging_level.
        level = _LEVEL_BY_VERBOSITY[args.verbosity]
    else:
        # Normally, we're not in debug mode, and there's not verbosity.
        level = LOGGING_LEVEL

    logger_kwargs = {"level": level, "devmode": args.dbg}
    init_logger(name="peppy", **logger_kwargs)
    global _LOGGER
    _LOGGER = init_logger(name=PKG_NAME, **logger_kwargs)

    if args.command == "convert":
        _LOGGER.debug("Creating a Project object from: {}".format(args.pep))
        p = Project(args.pep)
        convert_project(p, args.format)
        _LOGGER.info("Conversion successful")
        sys.exit(0)

    if args.command == "list":
        list_formats()
        sys.exit(0)

    sys.exit(0)