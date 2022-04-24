from os import system, name
import logging

from selenium import webdriver


logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s %(module)s -- %(funcName)s: %(message)s',
)
logger = logging.getLogger(__name__)


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def get_browser(url):
    logger.debug("Creating browser")
    fireFoxOptions = webdriver.FirefoxOptions()
    fireProfile = webdriver.FirefoxProfile()

    # in development always comment this line
    fireFoxOptions.add_argument('--headless')

    fireFoxOptions.set_preference('webdriver.load.strategy', 'unstable')
    browser = webdriver.Firefox(
        options=fireFoxOptions, firefox_profile=fireProfile)
    browser.delete_all_cookies()
    browser.get(url)
    logger.debug("Returning browser")
    return browser
