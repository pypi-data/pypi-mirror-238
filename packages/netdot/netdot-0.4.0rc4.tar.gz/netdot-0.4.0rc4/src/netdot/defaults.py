"""Default values to be used throughout this package.
"""
import os

TRUNCATE_MIN_CHARS: int = int(os.getenv('NETDOT_CLI_TRUNCATE_MIN', 20))
TERSE_COL_WIDTH: int = int(os.getenv('NETDOT_CLI_TERSE_COL_WIDTH', 16))
TERSE_MAX_CHARS: int = int(os.getenv(
    'NETDOT_CLI_TERSE_MAX_CHARS', 4 * TERSE_COL_WIDTH
))  # By default, allow up to 4 lines to print before truncating.
SKIP_SSL: bool = os.getenv('NETDOT_CLI_SKIP_SSL', 'FALSE').lower() == 'true'
VERIFY_SSL: bool = not SKIP_SSL
TIMEOUT: int = int(os.getenv('NETDOT_CLI_TIMEOUT', '20'))
RAISE_PARSE_ERRORS: bool = os.getenv('NETDOT_CLI_RAISE_PARSE_ERRORS', 'FALSE').lower() == 'true'
WARN_MISSING_FIELDS: bool = os.getenv('NETDOT_CLI_WARN_MISSING_FIELDS', 'TRUE').lower() == 'true'
THREADS: int = int(os.getenv('NETDOT_CLI_THREADS', 1))
