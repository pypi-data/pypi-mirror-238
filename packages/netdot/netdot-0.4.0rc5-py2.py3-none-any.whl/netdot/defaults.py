"""Default values to be used throughout this package.
"""
import sys
import configargparse
from typing import Dict, Any


def help():
    print(help_str())

def help_str():
    return (
        build_NETDOT_CLI_ENV_VARs_parser().format_help().replace('''
In general, command-line values override environment variables which override defaults.''', '')
        + """

> ⚠ NOTICE: These defaults are read from Environment Variables when this `netdot.defaults` module loads.
> Look for "[env var: NETDOT_CLI_...]" above to discover the available Environment Variables.
>
> Example: `export NETDOT_CLI_TERSE=True`
>
> Alternately, override these defaults by setting `netdot.defaults.<ENV_VAR_NAME>` directly in your code.
>
> Example: `netdot.defaults.TERSE=True`
"""
    )


def build_NETDOT_CLI_ENV_VARs_parser():
    parser = configargparse.ArgumentParser()
    parser.add_argument(
        '--terse',
        dest='TERSE',
        env_var='NETDOT_CLI_TERSE',
        type=bool,
        default=False,
        help='Print terse output (that generally tries to fit the screen width).',
    )
    parser.add_argument(
        '--truncate-min',
        dest='TRUNCATE_MIN_CHARS',
        env_var='NETDOT_CLI_TRUNCATE_MIN_CHARS',
        type=int,
        default=20,
        help='The absolute minimum number of characters to print before truncating.',
    )
    parser.add_argument(
        '--terse-col-width',
        dest='TERSE_COL_WIDTH',
        env_var='NETDOT_CLI_TERSE_COL_WIDTH',
        type=int,
        default=16,
        help='The number of characters to use for each column when printing terse output.',
    )
    parser.add_argument(
        '--terse-max-chars',
        dest='TERSE_MAX_CHARS',
        env_var='NETDOT_CLI_TERSE_MAX_CHARS',
        type=int,
        default=64,
        help='The maximum number of characters to print before truncating.',
    )
    parser.add_argument(
        '--skip-ssl',
        dest='SKIP_SSL',
        env_var='NETDOT_CLI_SKIP_SSL',
        type=bool,
        default=False,
        help='Skip SSL verification when making API requests.',
    )
    parser.add_argument(
        '--timeout',
        dest='TIMEOUT',
        env_var='NETDOT_CLI_TIMEOUT',
        type=int,
        default=20,
        help='''The number of seconds to wait for a response from the API 
        server. 
        Note: "timeout is not a time limit on the entire response download; 
        rather, an exception is raised if the server has not issued a response 
        for timeout seconds (more precisely, if no bytes have been received on 
        the underlying socket for timeout seconds). If no timeout is specified 
        explicitly, requests do not time out." (from requests.readthedocs.io)''',
    )
    parser.add_argument(
        '--raise-parse-errors',
        dest='RAISE_PARSE_ERRORS',
        env_var='NETDOT_CLI_RAISE_PARSE_ERRORS',
        type=bool,
        default=False,
        help='Raise an exception if there is an error parsing the response from the API server.',
    )
    parser.add_argument(
        '--warn-missing-fields',
        dest='WARN_MISSING_FIELDS',
        env_var='NETDOT_CLI_WARN_MISSING_FIELDS',
        type=bool,
        default=True,
        help='Warn if a field is missing from the response from the API server.',
    )
    parser.add_argument(
        '--threads',
        dest='THREADS',
        env_var='NETDOT_CLI_THREADS',
        type=int,
        default=1,
        help='The number of threads to use when making API GET requests.',
    )
    return parser


def parse_env_vars() -> Dict[str, Any]:
    """Parse all the environment variables that are used by this package.

    > Note: This function is called automatically when this module is imported.

    Returns:
        Dict: A dictionary of all the environment variables and their values.
    """
    args = vars(build_NETDOT_CLI_ENV_VARs_parser().parse_args([]))
    return args


# Export all the parsed env vars as variables in this module
this_module = sys.modules[__name__]
__all__ = list()
for env_var, value in parse_env_vars().items():
    setattr(this_module, env_var, value)
    __all__.append(env_var)

__all__.extend([
    'help',
    'help_str',
    'parse_env_vars',
])
