import pytest


def pytest_addoption(parser):
    parser.addoption('--poesessid', action='store', type=str, default=None, help='cookie from pathofexile.com')

def pytest_configure(config):
    pytest.poesessid = config.getoption('--poesessid')
