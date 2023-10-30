import random
from typing import Callable, Any

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.reports import TestReport


def pytest_addoption(parser: Parser):
    # Addoption doc: https://docs.python.org/uk/3/library/argparse.html#quick-links-for-add-argument # noqa
    parser.addoption(
        "--export",
        action="store_true",
        default=False,
        help="Provide to export results",
    )


def pytest_configure(config: Config):
    if config.getoption("--export"):
        config.pluginmanager.register(MyCoolExporter())


class MyCoolExporter:
    def __init__(self):
        self.result = []

    @staticmethod
    @pytest.fixture(autouse=True)
    def write_case_id(record_property: Callable[[str, Any], None]):
        rand = random.randint(1, 1000)
        record_property("case_id", f"my_cool_id_{rand}")

    def pytest_report_teststatus(self, report: TestReport):
        if report.when != "teardown":
            return

        case_id = [
            data[1] for data in report.user_properties if data[0] == "case_id"
        ]
        if case_id:
            self.result.append({"id": case_id, "result": report.outcome})

    def pytest_sessionfinish(self):
        print("Results to export:")
        print(self.result)
