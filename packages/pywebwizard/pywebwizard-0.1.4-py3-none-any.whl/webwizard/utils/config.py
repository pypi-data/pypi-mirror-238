from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

DEFAULT_TIMEOUT = 3

INTERFACES = {
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'css': By.CSS_SELECTOR,
    'class': By.CLASS_NAME,
    'tag': By.TAG_NAME,
    'link_text': By.LINK_TEXT,
    'link_text_partial': By.PARTIAL_LINK_TEXT
}

KEYBOARD = {
    'arrow_down': Keys.ARROW_DOWN,
    'arrow_left': Keys.ARROW_LEFT,
    'arrow_right': Keys.ARROW_RIGHT,
    'arrow_up': Keys.ARROW_UP,
    'backspace': Keys.BACKSPACE,
    'delete': Keys.DELETE,
    'end': Keys.END,
    'home': Keys.HOME,
    'insert': Keys.INSERT,
    'page_down': Keys.PAGE_DOWN,
    'page_up': Keys.PAGE_UP,
    'f1': Keys.F1,
    'f2': Keys.F2,
    'f3': Keys.F3,
    'f4': Keys.F4,
    'f5': Keys.F5,
    'f6': Keys.F6,
    'f7': Keys.F7,
    'f8': Keys.F8,
    'f9': Keys.F9,
    'f10': Keys.F10,
    'f11': Keys.F11,
    'f12': Keys.F12,
    'alt': Keys.ALT,
    'control': Keys.CONTROL,
    'shift': Keys.SHIFT,
    'command': Keys.COMMAND,
    'meta': Keys.META,
    'escape': Keys.ESCAPE,
    'space': Keys.SPACE,
    'tab': Keys.TAB,
    'enter': Keys.ENTER,
    'equals': Keys.EQUALS,
    'semicolon': Keys.SEMICOLON,
    'clear': Keys.CLEAR,
    'null': Keys.NULL
}

BROWSER_OPTIONS = {
    'firefox': {
        'options': Options,
        'webdriver': webdriver.Firefox
    },
    'chrome': {
        'options': webdriver.ChromeOptions,
        'webdriver': webdriver.Chrome
    }
}
