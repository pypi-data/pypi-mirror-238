from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as _ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from datetime import datetime
from copy import deepcopy
import requests
import time
import yaml
import json
import os

from .utils.exceptions import *
from .utils.config import INTERFACES, BROWSER_OPTIONS, DEFAULT_TIMEOUT, KEYBOARD
from .utils.functions import required_fields, is_valid_url
from .utils.logger import logging, logger


class SeleniumManagerBase:
    """
    Base class for Selenium management. It initializes the driver, handles configuration,
    and defines basic actions like clicking or filling fields.
    """

    def __init__(self, selenium_config_file: str, headers: dict = None, destruct_on_finish: bool = True):
        """
        Initializes the SeleniumManagerBase instance.

        :param selenium_config_file: Path to the configuration file or URL.
        :param headers: Optional headers for web requests.
        """
        self.driver = None
        self.actions, self.config = self._load_config(selenium_config_file)
        self.actions_map = {}
        self.headers = headers
        self.destruct_on_finish = self.config.get('destruct', destruct_on_finish)
        self.screenshots_dir = self.config.get('screenshots')
        if self.screenshots_dir and not os.path.isdir(self.screenshots_dir):
            os.mkdir(self.screenshots_dir)
        if not self.config:
            logging.error("Config not found")
            raise ConfigFileError("Config not found")
        self._driver_setup()
        if not self.driver:
            logging.error("Browser not found")
            raise BrowserError("Browser not found")

    def _load_config(self, selenium_config_file: str) -> tuple:
        """
        Loads the configuration from a file or URL.

        :param selenium_config_file: Path to the configuration file or URL.
        :return: Tuple containing actions and configuration dictionary.
        """
        if is_valid_url(selenium_config_file):
            return self._load_url_config(selenium_config_file)

        if not os.path.isfile(selenium_config_file):
            logging.error(f"File not found {selenium_config_file}")
            raise FileNotFoundError(f"File not found {selenium_config_file}")

        with open(selenium_config_file, 'r') as config:
            try:
                _data = yaml.safe_load(config)
                return _data.get('start', []), _data.get('config', {})
            except Exception as e:
                logging.error(f"Error loading config: {str(e)}")
                raise ConfigFormatError(f"Error loading config: {str(e)}")

    @staticmethod
    def _load_url_config(selenium_config_file_url: str) -> tuple:
        """
        Loads the configuration from a URL.

        :param selenium_config_file_url: The URL pointing to the YAML configuration file.
        :return: Tuple containing actions and configuration dictionary.
        """
        try:
            response = requests.get(selenium_config_file_url)
            if response.ok:
                try:
                    _data = yaml.safe_load(response.text)
                    return _data.get('start', []), _data.get('config', {})
                except yaml.YAMLError as e:
                    logging.error(f"Error reading YAML config file {selenium_config_file_url}: {str(e)}")
                    raise ConfigFormatError(f"Error reading YAML config file {selenium_config_file_url}: {str(e)}")
            else:
                logging.error(f"Error getting YAML config file {selenium_config_file_url}: Status Code {response.status_code}")
                raise ConfigFileError(f"Error getting YAML config file {selenium_config_file_url}: Status Code {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Error getting YAML config file {selenium_config_file_url}: {str(e)}")
            raise ConfigFileError(f"Error getting YAML config file {selenium_config_file_url}: {str(e)}")
        except Exception as e:
            logging.error(f"Something went wrong retrieving YAML config file {selenium_config_file_url}: {str(e)}")
            raise ConfigFileError(f"Something went wrong retrieving YAML config file {selenium_config_file_url}: {str(e)}")

    @staticmethod
    def _parse_action(action: dict):
        """
        Parses an action dictionary and extracts relevant information.

        :param action: Action dictionary.
        :return: Tuple with extracted information.
        """
        _interface = action.get('interface')
        _query = action.get('query')
        _timeout = action.get('timeout', DEFAULT_TIMEOUT)
        _index = action.get('index')
        if _index and _index < 1:
            _index = 1
        _content = action.get('content')
        _log = f"@body"
        if _interface and _query:
            _log = f"@{_interface}[query={_query}]{'' if not _index else '[' + str(_index) + ']'}"
        return _interface, _query, _timeout, _index, _content, _log

    @logger("info")
    def run_actions(self):
        """
        Starts the automated browser actions based on the loaded configuration.
        """
        try:
            for _action in self.actions:
                self._execute_action(_action)
                yield _action
        finally:
            if self.destruct_on_finish:
                self.driver.close()

    def _driver_setup(self):
        """
        Sets up the browser driver based on the configuration settings.
        """
        if self.config.get('browser') not in BROWSER_OPTIONS:
            raise BrowserError("Browser not supported")
        _browser_options = BROWSER_OPTIONS.get(self.config.get('browser', {}))
        _webdriver = _browser_options.get('webdriver')
        _options = _browser_options.get('options')
        if not _webdriver:
            raise BrowserError(f"Web Driver not found (allowed: {', '.join(BROWSER_OPTIONS.keys())})")
        _browser_options = _options()
        if self.config.get("hidden"):
            _browser_options.add_argument("--headless")
        self.driver = _webdriver(options=_browser_options)

    def _execute_action(self, action: dict):
        """
        Executes a single action.

        :param action: Action dictionary.
        """
        _action_name = action.get('action')
        if _action_name not in self.actions_map:
            raise ActionError(f"'{_action_name}' action not supported")
        self.actions_map.get(_action_name)(action)

    def _execute_js(self, *args, **kwargs):
        """
        Executes a JavaScript script in the context of the current session.

        :param args: Script and its arguments.
        :param kwargs: Optional keyword arguments for script execution.
        """
        self.driver.execute_script(*args, **kwargs)

    def _get_elements(self, interface: str, query: str, timeout: int = 10):
        """
        Retrieves web elements based on the specified search criteria.

        :param interface: Type of search (e.g., by ID, class, etc.).
        :param query: Search query or locator.
        :param timeout: Maximum time to wait for elements to appear.
        :return: Web elements.
        """
        _search = 'presence_of_element_located' if interface != INTERFACES.get(
            "class") else 'presence_of_all_elements_located'
        return WebDriverWait(self.driver, timeout).until(
            getattr(_ec, _search)((interface, query))
        )

    @staticmethod
    def _is_valid_interface(interface: str):
        if interface not in INTERFACES:
            raise InterfaceError("Interface not supported")
        return INTERFACES.get(interface)

    @staticmethod
    def _process_keys(keys_list: list) -> list:
        """
        Process a key, fetch from the KEYBOARD configuration if it's a special key.

        :param keys_list: The key to process.
        :return: Returns the key or raises ValueError if the key is not in the configuration.
        """
        keys_res = []
        for key in keys_list:
            _processed_key = KEYBOARD.get(key.lower())
            if _processed_key is None and len(key) == 1:
                _processed_key = key
            elif _processed_key is None:
                raise ValueError(f"Special key '{key}' not found in KEYBOARD configuration.")
            keys_res.append(_processed_key)
        return keys_res

    def _wait(self, interface: str, query: str, index: int = None, timeout: int = 10):
        """
        Waits for web elements to become available.

        :param interface: Type of search (e.g., by ID, class, etc.).
        :param query: Search query or locator.
        :param index: Index of the element to wait for (if expecting a list).
        :param timeout: Maximum time to wait for elements.
        :return: Single web element or list of web elements.
        """
        _interface = self._is_valid_interface(interface)
        _elements = self._get_elements(_interface, query, timeout)
        if isinstance(_elements, list):
            if not index:
                index = 1
            if len(_elements) > index - 1:
                return _elements[index - 1]
            return _elements[0]
        return _elements

    def _loop_file(self, action: dict):
        """
        Process a local file specified in the action dictionary. This method checks the file's existence and format,
        reads its JSON content, and initiates appropriate actions based on its content.

        :param action: Dictionary containing details about the action to be performed.
                       It must include a 'source' key with the path to the file.
        :raises FileNotFoundError: If the file specified in the action's 'source' does not exist.
        :raises ValueError: If the file provided is not in JSON format.
        """
        _do_source = action.get('source')
        if not os.path.isfile(_do_source):
            raise FileNotFoundError(f"File not found {_do_source}")
        if not _do_source.endswith('.json'):
            raise ValueError(f"File format not found. Should be JSON format. ({_do_source})")
        _file_values = json.load(open(_do_source, 'r', encoding='utf-8'))
        self._do_file_actions(action, _file_values)

    def _loop_web_file(self, action: dict):
        """
        Retrieve and process a file from the web specified in the action dictionary. This method attempts to download the
        file, expecting a JSON response, and initiates appropriate actions based on its content.

        :param action: Dictionary containing details about the action to be performed.
                       It must include a 'source' key with the URL to the file.
        :raises requests.RequestException: If there is a network problem, like a DNS failure, refused connection, etc.
        :raises ValueError: If the response from the 'source' does not contain valid JSON.
        """
        try:
            response = requests.get(action.get('source'))
            if response.ok or response.is_redirect:
                try:
                    self._do_file_actions(action, response.json())
                except ValueError as e:
                    logging.error("The response of the source does not contain JSON type data")
        except requests.RequestException as e:
            logging.error(f"Something went wrong retrieving data from {action.get('source')}: {str(e)}")
        except Exception as e:
            logging.error(f"Something went wrong: {str(e)}")

    def _do_file_actions(self, action: dict, file_data: dict):
        """
        Execute the commands specified in the 'do' section of the action dictionary, applying them to the provided file_data.

        :param action: Dictionary containing details about the actions to be performed.
        :param file_data: Dictionary parsed from a JSON file, containing data the actions will be applied to.
        """
        for _file_action in file_data:
            for _action in deepcopy(action.get('do', [])):
                for _action_key, _action_value in _action.items():
                    if isinstance(_action_value, str) and _action_value.startswith('do__'):
                        _key = _action_value.removeprefix('do__')
                        if _get_value := _file_action.get(_key):
                            _action[_action_key] = _get_value
                self._execute_action(_action)

    def send_keys_to_element(self, element, keys: list):
        """
        Helper method to send keys to the element. If no element is specified, it sends keys to the body or active element.

        :param element: The web element to send keys to, could be None for sending keys to the active element.
        :param keys: The key action to send.
        """
        if element:
            element.send_keys(*keys)
        else:
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(*keys)
            except WebDriverException as e:
                logging.error(f"An error occurred while sending keys to the active element: {str(e)}")
                raise


class SeleniumManager(SeleniumManagerBase):
    """
    Manages advanced Selenium actions such as navigation, clicks, input filling, screenshots, scrolling,
    and more, extending the base functionality provided by SeleniumManagerBase.

    :param selenium_config_file: Path to the Selenium configuration file.
    :param headers: Optional dictionary of headers to be used in the web requests.
    """

    def __init__(self, selenium_config_file: str, headers: dict = None):
        """
        Initializes the SeleniumManager with a specific configuration file and optional headers.

        :param selenium_config_file: Path to the Selenium configuration file.
        :param headers: Optional dictionary of headers for web requests.
        """
        super().__init__(selenium_config_file, headers)
        self.actions_map = {
            'navigate': self._navigate,
            'click': self._click,
            'fill': self._fill,
            'screenshot': self._screenshot,
            'scroll': self._scroll,
            'sleep': self._sleep,
            'loop': self._loop,
            'keyboard': self._keyboard,
            'execute': self._execute_js_action
        }

    @required_fields(['do'])
    def _loop(self, action: dict):
        """
        Executes actions in a loop, which can be based on a fixed number of times or iteratively over
        content from a web source.

        :param action: Dictionary specifying the details of the loop action.
        :raises LoopError: If neither 'times' nor 'source' is specified in the action.
        """
        if not any(action.get(_mode) for _mode in ['times', 'source']):
            raise LoopError("Times or source have to be defined in 'loop' action")
        if _do_times := action.get('times'):
            for _ in range(int(action.get('times'))):
                for _action in action.get('do', []):
                    self._execute_action(_action)
            return
        if is_valid_url(action.get('source')):
            return self._loop_web_file(action)
        return self._loop_file(action)

    @required_fields(['interface', 'query'])
    def _click(self, action: dict):
        """
        Performs a click action on a web element identified by a specific interface and query.

        :param action: Dictionary containing parameters for the click action, including 'interface' and 'query'.
        """
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        logging.info(f"[CLICK] {_log}")
        _element = self._wait(_interface, _query, _index, _timeout)
        _element.click()

    @required_fields(['interface', 'query', 'content'])
    def _fill(self, action: dict):
        """
        Finds a web element and fills it with content. Requires the web element's interface, query, and the content to fill.

        :param action: Dictionary containing parameters for the fill action.
        """
        _interface, _query, _timeout, _index, _content, _log = self._parse_action(action)
        _field = self._wait(_interface, _query, _index, _timeout)
        logging.info(f"[FILL] {_log}")
        _field.send_keys(_content)

    @required_fields(['url'])
    def _navigate(self, action: dict):
        """
        Navigates the browser to a specified URL.

        :param action: Dictionary containing the URL for navigation.
        """
        logging.info(f"[NAVIGATE] {action.get('url')}")
        self.driver.get(action.get('url'))

    @required_fields(['time'])
    def _sleep(self, action: dict):
        """
        Pauses the execution for a specified number of seconds.

        :param action: Dictionary containing the number of seconds to sleep.
        """
        time.sleep(int(action.get('time')))

    @required_fields(['file_name'])
    def _screenshot(self, action: dict):
        """
        Takes a screenshot of the current browser window, with optional additional CSS styling.

        :param action: Dictionary specifying the screenshot parameters, including optional CSS styling.
        :raises ScreenshotError: If 'style' is not defined for an element in the 'css' section of the action.
        """
        _file_name = f"{action.get('file_name')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        _photo_name = os.path.join(self.screenshots_dir, _file_name)
        if _styles := action.get('css'):
            for _element in _styles:
                if not _element.get('style'):
                    raise ScreenshotError("Style not defined in 'screenshot' css defined element")

                _element_instance = self._wait(_element.get('interface'), _element.get('query'))
                self._execute_js("arguments[0].setAttribute('style', arguments[1]);", _element_instance, _element.get('style'))
            time.sleep(.2)
        logging.info(f"[SCREENSHOT] {_photo_name}")
        self.driver.save_screenshot(_photo_name)

    def _scroll(self, action: dict):
        """
        Scrolls the webpage by a specified amount along the x and y axes.

        :param action: Dictionary containing the 'x' and 'y' scroll values.
        :raises ScrollError: If either 'x' or 'y' is not defined in the action.
        """
        _movement = (action.get('x'), action.get('y'))
        if all([m is None for m in _movement]):
            raise ScrollError("X or Y need to be defined in 'scroll' action")
        if _movement[0] is None:
            _movement = 0, _movement[1]
        if _movement[1] is None:
            _movement = _movement[0], 0
        logging.info(f"[SCROLL] ({_movement})")
        self._execute_js(f"window.scrollBy{_movement};")

    @required_fields(['js'])
    def _execute_js_action(self, action: dict):
        logging.info("[EXECUTING JS]")
        if _js_action := action.get('js'):
            logging.info(f"[JS] {_js_action}")
            self._execute_js(_js_action)

    @required_fields(['interface', 'query'])
    def _submit(self, action: dict):
        """
        Submits a form on the webpage based on the provided selector.

        :param action: Dictionary containing parameters for the submit action, including 'interface' and 'query'.
        """
        _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
        logging.info(f"[SUBMIT] {_log}")
        _form = self._wait(_interface, _query, _index, _timeout)
        _form.submit()

    @required_fields(['keys'])
    def _keyboard(self, action: dict):
        try:
            _interface, _query, _timeout, _index, _, _log = self._parse_action(action)
            _keys = action.get('keys', [])

            if not _keys:
                raise ValueError("The 'keys' field is required for keyboard actions.")

            if (_interface and not _query) or (_query and not _interface):
                raise ValueError(
                    "Both 'interface' and 'query' should be provided together, or neither should be present.")

            logging.info(f"[KEYBOARD] {_log}")

            _element = None
            if _interface and _query:
                _interface = self._is_valid_interface(_interface)
                _element = self._wait(_interface, _query)

            _processed_keys = self._process_keys(_keys)

            action_chain = ActionChains(self.driver)

            logging.info(f"[KEYBOARD] [PRESS] {' + '.join([_k.capitalize() for _k in _keys])}")

            for key in _processed_keys:
                action_chain.key_down(key)

            for key in reversed(_processed_keys):
                action_chain.key_up(key)

            action_chain.perform()

        except NoSuchElementException as e:
            logging.error(f"Element not found when trying to perform keyboard action: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while performing a keyboard action: {str(e)}")
            raise
