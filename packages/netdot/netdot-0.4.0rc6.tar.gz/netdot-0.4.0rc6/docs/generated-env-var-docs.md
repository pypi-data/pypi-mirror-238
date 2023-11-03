
<a id="netdot-python-api-environment-variables"></a>

# Netdot Python API Environment Variables

> Generated using `netdot.defaults.help()`
>
> Version 0.4.0 documentation generated on Nov 02, 2023 at 03:50PM 

```
usage: __main__.py [-h] [--terse TERSE] [--truncate-min TRUNCATE_MIN_CHARS]
                   [--terse-col-width TERSE_COL_WIDTH]
                   [--terse-max-chars TERSE_MAX_CHARS] [--skip-ssl SKIP_SSL]
                   [--timeout TIMEOUT]
                   [--raise-parse-errors RAISE_PARSE_ERRORS]
                   [--warn-missing-fields WARN_MISSING_FIELDS]
                   [--threads THREADS]

optional arguments:
  -h, --help            show this help message and exit
  --terse TERSE         Print terse output (that generally tries to fit the
                        screen width). [env var: NETDOT_CLI_TERSE]
  --truncate-min TRUNCATE_MIN_CHARS
                        The absolute minimum number of characters to print
                        before truncating. [env var:
                        NETDOT_CLI_TRUNCATE_MIN_CHARS]
  --terse-col-width TERSE_COL_WIDTH
                        The number of characters to use for each column when
                        printing terse output. [env var:
                        NETDOT_CLI_TERSE_COL_WIDTH]
  --terse-max-chars TERSE_MAX_CHARS
                        The maximum number of characters to print before
                        truncating. [env var: NETDOT_CLI_TERSE_MAX_CHARS]
  --skip-ssl SKIP_SSL   Skip SSL verification when making API requests. [env
                        var: NETDOT_CLI_SKIP_SSL]
  --timeout TIMEOUT     The number of seconds to wait for a response from the
                        API server. Note: "timeout is not a time limit on the
                        entire response download; rather, an exception is
                        raised if the server has not issued a response for
                        timeout seconds (more precisely, if no bytes have been
                        received on the underlying socket for timeout
                        seconds). If no timeout is specified explicitly,
                        requests do not time out." (from
                        requests.readthedocs.io) [env var: NETDOT_CLI_TIMEOUT]
  --raise-parse-errors RAISE_PARSE_ERRORS
                        Raise an exception if there is an error parsing the
                        response from the API server. [env var:
                        NETDOT_CLI_RAISE_PARSE_ERRORS]
  --warn-missing-fields WARN_MISSING_FIELDS
                        Warn if a field is missing from the response from the
                        API server. [env var: NETDOT_CLI_WARN_MISSING_FIELDS]
  --threads THREADS     The number of threads to use when making API GET
                        requests. [env var: NETDOT_CLI_THREADS]

 In general, command-line values override environment variables which override
defaults.


> ⚠ NOTICE: These defaults are read from Environment Variables when this `netdot.defaults` module loads.
> Look for "[env var: NETDOT_CLI_...]" above to discover the available Environment Variables.
>
> Example: `export NETDOT_CLI_TERSE=True`
>
> Alternately, override these defaults by setting `netdot.defaults.<ENV_VAR_NAME>` directly in your code.
>
> Example: `netdot.defaults.TERSE=True`

```
