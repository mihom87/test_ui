import copy
import json
import logging
import shutil
from pathlib import Path

import allure
import pytest
import requests
from faker import Faker

from ext_selenium.a11y import PyleniumAxe
from ext_selenium.config import PyleniumConfig, TestCase
from ext_selenium.driver import Pylenium


@pytest.fixture(scope="function")
def fake() -> Faker:
    """A basic instance of Faker to make test data."""
    return Faker()


@pytest.fixture(scope="function")
def api():
    """A basic instance of Requests to make HTTP API calls."""
    return requests


@pytest.fixture(scope="session", autouse=True)
def project_root() -> Path:
    """The Project (or Workspace) root as a filepath.

    * This conftest.py file should be in the Project Root if not already.
    """
    return Path(__file__).absolute().parent


@pytest.fixture(scope="session", autouse=True)
def test_results_dir(project_root: Path, request) -> Path:
    """Creates the `/test_results` directory to store the results of the Test Run.

    Returns:
        The `/test_results` directory as a filepath (str).
    """
    session = request.node
    test_results_dir = project_root.joinpath("test_results")

    if test_results_dir.exists():
        # delete /test_results from previous Test Run
        shutil.rmtree(test_results_dir, ignore_errors=True)

    try:
        # race condition can occur between checking file existence and
        # creating the file when using pytest with multiple workers
        test_results_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass

    for test in session.items:
        try:
            # make the test_result directory for each test
            test_results_dir.joinpath(test.name).mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass

    return test_results_dir


@pytest.fixture(scope="session")
def _load_pylenium_json(project_root, request) -> PyleniumConfig:
    """Load the default pylenium.json file or the given pylenium.json config file (if specified).

    * Pylenium looks for these files from the Project Root!

    I may have multiple pylenium.json files with different presets. For example:
    - stage-pylenium.json
    - dev-testing.json
    - firefox-pylenium.json

    Examples
    --------
    $ pytest
    >>> Loads the default file: PROJECT_ROOT/pylenium.json

    $ pytest pylenium_json=dev-pylenium.json
    >>> Loads the config file: PROJECT_ROOT/dev-pylenium.json

    $ pytest pylenium_json="configs/stage-pylenium.json"
    >>> Loads the config file: PROJECT_ROOT/configs/stage-pylenium.json
    """
    custom_config_filepath = request.config.getoption("pylenium_json")
    config_filepath = project_root.joinpath(custom_config_filepath or "pylenium.json")

    try:
        with config_filepath.open() as file:
            _json = json.load(file)
        config = PyleniumConfig(**_json)
    except FileNotFoundError:
        logging.warning(f"The config_filepath was not found, so PyleniumConfig will load with default values. File not found: {config_filepath.absolute()}")
        config = PyleniumConfig()

    return config


@pytest.fixture(scope="session")
def _override_pylenium_config_values(_load_pylenium_json: PyleniumConfig, request) -> PyleniumConfig:
    """Override any PyleniumConfig values after loading the initial pylenium.json config file.

    After a pylenium.json config file is loaded and converted to a PyleniumConfig object,
    then any CLI arguments override their respective key/values.
    """
    config = _load_pylenium_json
    # Driver Settings
    cli_remote_url = request.config.getoption("--remote_url")
    if cli_remote_url:
        config.driver.remote_url = cli_remote_url

    cli_browser_options = request.config.getoption("--options")
    if cli_browser_options:
        config.driver.options = [option.strip() for option in cli_browser_options.split(",")]

    cli_browser = request.config.getoption("--browser")
    if cli_browser:
        config.driver.browser = cli_browser

    cli_local_path = request.config.getoption("--local_path")
    if cli_local_path:
        config.driver.local_path = cli_local_path

    cli_capabilities = request.config.getoption("--caps")
    if cli_capabilities:
        # --caps must be in '{"name": "value", "boolean": true}' format
        # with double quotes around each key. booleans are lowercase.
        config.driver.capabilities = json.loads(cli_capabilities)

    cli_wire_enabled = request.config.getoption("--wire_enabled")
    if cli_wire_enabled:
        # --wire_enabled is false unless they specify "true"
        wire_enabled = cli_wire_enabled.lower() == "true"
        config.driver.seleniumwire_enabled = wire_enabled

    cli_wire_options = request.config.getoption("--wire_options")
    if cli_wire_options:
        # --wire_options must be in '{"name": "value", "boolean": true}' format
        # with double quotes around each key. booleans are lowercase.
        config.driver.seleniumwire_options = json.loads(cli_wire_options)

    cli_page_wait_time = request.config.getoption("--page_load_wait_time")
    if cli_page_wait_time and cli_page_wait_time.isdigit():
        config.driver.page_load_wait_time = int(cli_page_wait_time)

    # Logging Settings
    cli_screenshots_on = request.config.getoption("--screenshots_on")
    if cli_screenshots_on:
        shots_on = cli_screenshots_on.lower() == "true"
        config.logging.screenshots_on = shots_on

    cli_extensions = request.config.getoption("--extensions")
    if cli_extensions:
        config.driver.extension_paths = [ext.strip() for ext in cli_extensions.split(",")]

    cli_log_level = request.config.getoption("--pylog_level")
    if cli_log_level:
        level = cli_log_level.upper()
        config.logging.pylog_level = level if level in ["DEBUG", "COMMAND", "INFO", "USER", "WARNING", "ERROR", "CRITICAL"] else "INFO"

    return config


@pytest.fixture(scope="function")
def py_config(_override_pylenium_config_values) -> PyleniumConfig:
    """Get a fresh copy of the PyleniumConfig for each test

    See _load_pylenium_json and _override_pylenium_config_values for how the initial configuration is read.
    """
    return copy.deepcopy(_override_pylenium_config_values)


@pytest.fixture(scope="class")
def pyc_config(_override_pylenium_config_values) -> PyleniumConfig:
    """Get a fresh copy of the PyleniumConfig for each test class"""
    return copy.deepcopy(_override_pylenium_config_values)


@pytest.fixture(scope="session")
def pys_config(_override_pylenium_config_values) -> PyleniumConfig:
    """Get a fresh copy of the PyleniumConfig for each test session"""
    return copy.deepcopy(_override_pylenium_config_values)


@pytest.fixture(scope="function")
def test_case(test_results_dir: Path, request) -> TestCase:
    """Manages data pertaining to the currently running Test Function or Case.

        * Creates the test-specific logger.

    Args:
        test_results_dir: The ./test_results directory this Test Run (aka Session) is writing to

    Returns:
        An instance of TestCase.
    """
    test_name = request.node.name
    test_result_path = test_results_dir.joinpath(test_name)
    return TestCase(name=test_name, file_path=test_result_path)


@pytest.fixture(scope="function")
def py(test_case: TestCase, py_config: PyleniumConfig, request):
    """Initialize a Pylenium driver for each test.

    Pass in this `py` fixture into the test function.

    Examples:
        def test_go_to_google(py):
            py.visit('https://google.com')
            assert 'Google' in py.title()
    """
    py = Pylenium(py_config)
    yield py
    try:
        if request.node.report.failed:
            # if the test failed, execute code in this block
            if py_config.logging.screenshots_on:
                screenshot = py.screenshot(str(test_case.file_path.joinpath("test_failed.png")))
                allure.attach(screenshot, "test_failed.png", allure.attachment_type.PNG)

        elif request.node.report.passed:
            # if the test passed, execute code in this block
            pass
        else:
            # if the test has another result (ie skipped, inconclusive), execute code in this block
            pass
    except Exception:
        logging.error("Failed to take screenshot on test failure.")
    py.quit()


@pytest.fixture(scope="class")
def pyc(pyc_config: PyleniumConfig, request):
    """Initialize a Pylenium driver for an entire test class."""
    py = Pylenium(pyc_config)
    yield py
    try:
        if request.node.report.failed:
            # if the test failed, execute code in this block
            if pyc_config.logging.screenshots_on:
                allure.attach(py.webdriver.get_screenshot_as_png(), "test_failed.png", allure.attachment_type.PNG)
        elif request.node.report.passed:
            # if the test passed, execute code in this block
            pass
        else:
            # if the test has another result (ie skipped, inconclusive), execute code in this block
            pass
    except Exception:
        logging.error("Failed to take screenshot on test failure.")
    py.quit()


@pytest.fixture(scope="session")
def pys(pys_config: PyleniumConfig, request):
    """Initialize a Pylenium driver for an entire test session."""
    py = Pylenium(pys_config)
    yield py
    try:
        if request.node.report.failed:
            # if the test failed, execute code in this block
            if pys_config.logging.screenshots_on:
                allure.attach(py.webdriver.get_screenshot_as_png(), "test_failed.png", allure.attachment_type.PNG)
        elif request.node.report.passed:
            # if the test passed, execute code in this block
            pass
        else:
            # if the test has another result (ie skipped, inconclusive), execute code in this block
            pass
    except Exception:
        logging.error("Failed to take screenshot on test failure.")
    py.quit()


@pytest.fixture(scope="function")
def axe(py) -> PyleniumAxe:
    """The aXe A11y audit tool as a fixture."""
    return PyleniumAxe(py.webdriver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Yield each test's outcome so we can handle it in other fixtures."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        setattr(item, "report", report)
    return report


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="", help="The lowercase browser name: chrome | firefox")
    parser.addoption("--local_path", action="store", default="", help="The filepath to the local driver")
    parser.addoption("--remote_url", action="store", default="", help="Grid URL to connect tests to.")
    parser.addoption("--screenshots_on", action="store", default="", help="Should screenshots be saved? true | false")
    parser.addoption(
        "--pylenium_json",
        action="store",
        default="",
        help="The filepath of the pylenium.json file to use (ie dev-pylenium.json)",
    )
    parser.addoption(
        "--pylog_level", action="store", default="INFO", help="Set the logging level: 'DEBUG' | 'COMMAND' | 'INFO' | 'USER' | 'WARNING' | 'ERROR' | 'CRITICAL'"
    )
    parser.addoption(
        "--options",
        action="store",
        default="",
        help='Comma-separated list of Browser Options. Ex. "headless, incognito"',
    )
    parser.addoption(
        "--caps",
        action="store",
        default="",
        help='List of key-value pairs. Ex. \'{"name": "value", "boolean": true}\'',
    )
    parser.addoption(
        "--page_load_wait_time",
        action="store",
        default="",
        help="The amount of time to wait for a page load before raising an error. Default is 0.",
    )
    parser.addoption("--extensions", action="store", default="", help='Comma-separated list of extension paths. Ex. "*.crx, *.crx"')
    parser.addoption(
        "--wire_enabled",
        action="store",
        default=False,
        help="Should the Wire Protocol be enabled? true | false",
    )
    parser.addoption(
        "--wire_options",
        action="store",
        default="",
        help='Dict of key-value pairs as a string. Ex. \'{"name": "value", "boolean": true}\'',
    )
