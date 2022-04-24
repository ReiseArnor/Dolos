from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from dolos.servers.baseclass import Server
from dolos.util import clear_screen, logger


class Fembed(Server):

    def __init__(self, url):
        self.url = url
        logger.info(f"self.url {self.url}")

    def get_video_link(self, browser):
        browser.get(self.url)
        logger.debug("Waiting for redirect..")
        Wait(browser, 5).until(EC.url_changes("https://diasfem.com"))
        logger.debug("Redirected")

        self._clicks_pre_link(browser)

        quality = True
        if quality:
            self.select_quality(browser)

        try:
            video_link = Wait(browser, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='jw-video jw-reset']"))).get_attribute('src')

        except:
            logger.error("couldn't load video_link")
            browser.quit()
            exit(2)

        return video_link

    def select_quality(self, browser):
        try:
            Wait(browser, 2).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@button='qSwitch']"))).click()
            Wait(browser, 2).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[text()='720p']"))).click()

        except:
            logger.info("No se encontraron las opciones de calidad de video")
            # raise

    def _clicks_pre_link(self, browser):
        logger.debug("current_url " + browser.current_url)
        try:
            blank_block1 = Wait(browser, 5).until(
                EC.visibility_of_element_located((By.TAG_NAME, "body")))
            blank_block1.click()

            blank_block2 = Wait(browser, 5).until(
                EC.visibility_of_element_located((By.ID, "loading")))
            blank_block2.click()

        except:
            taken_down = Wait(browser, 1).until(EC.visibility_of_element_located(
                (By.XPATH, "//p[text()='Sorry this video is unavailable: DMCA Takedown']"))).is_enabled()
            if taken_down:
                browser.quit()
                logger.error(
                    "Lo siento el video fue dado de baja en el servidor fembed. Intenta con otro servidor.")
                exit(2)

            raise
