from dotenv import load_dotenv

from infra.config.config_provider import init_config


load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="config.ini")


def pytest_configure(config):
    init_config(config.getoption('--config'))
