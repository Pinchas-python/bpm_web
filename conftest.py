from infra.config.config_provider import init_config

config_path = ""
browser = {}


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="config.ini")


def pytest_configure(config):
    config_path = config.getoption('--config')
    init_config(config_path)
