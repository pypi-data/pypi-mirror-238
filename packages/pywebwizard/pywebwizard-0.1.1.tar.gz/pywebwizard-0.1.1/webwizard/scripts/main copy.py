from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import selenium
import json
import sys
import time
import yaml
import os

from utils.logger import logging
from utils.config import INTERFACES, BROWSER_OPTIONS, DEFAULT_TIMEOUT

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

config_file = 'config.yaml'

def logger(log_type: str):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            getattr(logging, log_type)("Start function")
            f(*args, **kwargs)
            getattr(logging, log_type)("End function")
        return wrapped
    return wrapper


class ConfigFormatError(Exception):
    pass


class SeleniumManager:

    def __init__(self, selenium_config_file: str):
        self.driver = None
        self.actions, self.config = self.__load_config__(selenium_config_file)
        self.actions_map = {
            'navigate': self._navigate,
            'click': self._click,
            'fill': self._fill,
            'screenshot': self._screenshot,
            'scroll': self._scroll
        }
        self.screenshots_dir = self.config.get('screenshots')
        if self.screenshots_dir and not os.path.isdir(self.screenshots_dir):
            os.mkdir(self.screenshots_dir)

    @staticmethod
    def __load_config__(selenium_config_file: str) -> dict:
        if not os.path.isfile(selenium_config_file):
            raise FileNotFoundError(f"File not found {selenium_config_file}")

        with open(selenium_config_file, 'r') as config:
            try:
                _data = yaml.safe_load(config)
                return _data.get('start', []), _data.get('config', {})
            except Exception as e:
                raise ConfigFormatError(f"Error loading config: {str(e)}")

    @logger("info")
    def start(self):
        logging.info("Starting automation")
        if not self.config:
            raise ValueError("Config not found")

        self.__driver_setup__()

        if not self.driver:
            raise ValueError("Browser not found")

        try:
            self._execute()
        finally:
            self.driver.close()


    def __keyboard__(self, keys: list, element: object = None):
        if not element:
            element = self.driver.find_element_by_tag_name('body')
        logging.info(f"Sending keys: {keys}")
        element.send_keys(*keys)

    def __driver_setup__(self):
        assert self.config.get('browser') in BROWSER_OPTIONS, "Browser not supported"
        _browser_options = BROWSER_OPTIONS.get(self.config.get('browser', {}))
        _webdriver = _browser_options.get('webdriver')
        _options = _browser_options.get('options')
        assert _webdriver, "Web Driver not found"
        _browser_options = _options()
        if self.config.get("hidden"):
            _browser_options.add_argument("--headless")
        self.driver = _webdriver(options=_browser_options)

    def _execute(self):
        for _action in self.actions:
            _action_name = _action.get('action')
            assert _action_name in self.actions_map, "Action not supported"
            if _action_name == 'navigate':
                assert _action.get('url'), "URL not defined for 'navigate' action"
                self._navigate(_action.get('url'))
                continue
            if _action_name == 'screenshot':
                assert _action.get('file_name'), "File name not defined for 'screenshot' action"
                self._screenshot(_action.get('file_name'), _action.get('css', []))
                continue
            if _action_name == 'scroll':
                assert _action.get("x") or _action.get("y"), "X or Y need to be defined in 'scroll' action"
                self._scroll((_action.get("x"), _action.get("y")))
                continue
            _interface = _action.get('interface')
            _query = _action.get('query')
            _timeout = _action.get('timeout', DEFAULT_TIMEOUT)
            _index = _action.get('index', 1)
            if _index < 1:
                _index = 1
            _content = _action.get('content')
            assert _query is not None, f"Query needed for this action ({_action_name})"
            if _content:
                self.actions_map.get(_action_name)(_interface, _query, _index, _content, _timeout)
            else:
                self.actions_map.get(_action_name)(_interface, _query, _index, _timeout)

    def _execute_js(self, *args, **kwargs):
        self.driver.execute_script(*args, **kwargs)
        
    def _click(self, interface: str, query: str, index: int = 1, timeout: int = 10):
        logging.info(f"Clicking element with interface: {interface}, query: {query}, index: {index}")
        _element = self._wait(interface, query, index, timeout)
        _element.click()

    def _get_elements(self, interface: str, query: str, timeout: int = 10):
        _search = 'presence_of_element_located' if interface != INTERFACES.get(
            "class") else 'presence_of_all_elements_located'
        return WebDriverWait(self.driver, timeout).until(
            getattr(EC, _search)((interface, query))
        )

    def _wait(self, interface: str, query: str, index: int = 1, timeout: int = 10):
        assert interface in INTERFACES, "Interface not supported"
        _interface = INTERFACES.get(interface)
        _elements = self._get_elements(_interface, query, timeout)
        if isinstance(_elements, list):
            if len(_elements) > index - 1:
                return _elements[index - 1]
            return _elements[0]
        return _elements

    def _fill(self, interface: str, query: str, index: int = 1, content: str = "", timeout: int = 10):
        _field = self._wait(interface, query, index, timeout)
        logging.info(f"Filling an element with this text: {content}")
        _field.send_keys(content)

    def _navigate(self, url):
        logging.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def _submit(self):
        # TODO: Implementation for the submit action, if needed.
        pass

    def _scroll(self, movement: tuple = (0, 200)):
        logging.info(f"Scrolling x: {movement[0]} & y: {movement[1]}")
        self._execute_js(f"window.scrollBy{movement};")

    def _screenshot(self, file_name: str, styles: list = []):
        _file_name = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        _photo_name = os.path.join(self.screenshots_dir, _file_name)
        for _element in styles:
            if not _element.get('style'):
                raise ValueError("Style not defined in 'screenshot' css defined element")

            _element_instance = self._wait(_element.get('interface'), _element.get('query'))
            self._execute_js("arguments[0].setAttribute('style', arguments[1]);", _element_instance, _element.get('style'))
        if styles:
            time.sleep(.2)
        logging.info(f"Screenshot saved:{_photo_name}")
        self.driver.save_screenshot(_photo_name)




class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Selenium Manager'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()

        self.load_config_button = QPushButton('Cargar Configuración')
        self.load_config_button.clicked.connect(self.load_config)
        layout.addWidget(self.load_config_button)

        self.navigate_button = QPushButton('Navegar')
        self.navigate_button.clicked.connect(self.navigate)
        layout.addWidget(self.navigate_button)

        self.click_button = QPushButton('Click')
        self.click_button.clicked.connect(self.click)
        layout.addWidget(self.click_button)

        self.setLayout(layout)
        self.show()

    def load_config(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Cargar archivo de configuración", "", "YAML Files (*.yaml);;All Files (*)", options=options)
        if fileName:
            self.selenium_manager = SeleniumManager(fileName)

    def navigate(self):
        if hasattr(self, 'selenium_manager'):
            self.selenium_manager.start()

    def click(self):
        # Aquí podrías ejecutar una acción específica de click en lugar de todo el flujo
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    # browser = SeleniumManager(config_file)
    # browser.start()
