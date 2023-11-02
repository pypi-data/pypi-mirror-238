from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.python import Function
from _pytest.runner import CallInfo


def pytest_addoption(parser: Parser):
    # Addoption doc: https://docs.python.org/uk/3/library/argparse.html#quick-links-for-add-argument # noqa
    parser.addoption(
        "--extra-log",
        action="store_true",
        default=False,
        help="Provide to extend logging",
    )


def pytest_configure(config: Config):
    if config.getoption("--extra-log"):
        config.pluginmanager.register(MyCoolLoggerForPytest())


class MyCoolLoggerForPytest:
    @staticmethod
    def pytest_runtest_setup(item: Function):
        total_tests = len(item.session.items)
        current_index = item.session.items.index(item) + 1
        text = f"Running test {item.name} ({current_index} of {total_tests})"
        print("\n" + text.center(80, "="))

    @staticmethod
    def pytest_runtest_makereport(call: CallInfo):
        print(f"Stage '{call.when}' has finished")

    @staticmethod
    def pytest_sessionfinish():
        print("Test session finished!")
