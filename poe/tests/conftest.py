import pytest


def pytest_addoption(parser):
    parser.addoption("--poesessid", action="store", type="string", default=None, help='cookie from pathofexile.com')

def pytest_configure(config):
    pytest.poesessid = config.getoption('poesessid')