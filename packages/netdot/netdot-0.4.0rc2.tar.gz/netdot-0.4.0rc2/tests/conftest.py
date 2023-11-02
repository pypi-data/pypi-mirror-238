import os

import pytest

import netdot


@pytest.fixture
def netdot_url() -> str:
    return os.environ.get("NETDOT_URL", "https://nsdb.uoregon.edu")


@pytest.fixture
def username() -> str:
    return os.environ.get("NETDOT_USERNAME", "not-defined-NETDOT_USERNAME-env-var")


@pytest.fixture
def password() -> str:
    return os.environ.get("NETDOT_PASSWORD", "not-defined-NETDOT_PASSWORD-env-var")


@pytest.fixture
def repository(netdot_url, username, password) -> netdot.Repository:
    return netdot.Repository(
        netdot_url, username, password, threads=1, times_to_retry=0, timeout=5  # seconds
    )


@pytest.fixture(scope='module')
def vcr_config():
    return {
        'before_record_request': [sanitize_NetdotLogin_path],
        'before_record_response': [ignore_redirected_html_after_login],
    }


def ignore_redirected_html_after_login(response):
    """We do not care about responses that start with <html>.

    We are testing data APIs, and this makes the cassettes much more readable to ignore the HTML pages returned.
    """
    try:
        if response['body']['string'].strip().startswith(b'<html>'):
            response['body']['string'] = 'HTML content ignored (see conftest.py)'
    except TypeError:
        pass
    return response


def sanitize_NetdotLogin_path(request):
    """Clear the "body" of the request if it is sent to the /NetdotLogin path."""
    if request.path == '/NetdotLogin':
        request.body = 'BLANK (see conftest.py)'
    return request
