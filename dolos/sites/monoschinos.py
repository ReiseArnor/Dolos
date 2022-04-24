import re
from sys import exit

from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from dolos.sites.baseclass import Site
from dolos.util import clear_screen, get_browser, logger


class Monoschinos(Site):

    @property
    def base_url(self):
        return "https://monoschinos2.com"

    def setup(self, anime, episode, server):
        self.anime = anime
        self.episode = episode
        self.server = server

    def search(self):
        self.formatted_anime = self.anime.replace(' ', '-')
        browser = get_browser(
            f"{self.base_url}/buscar?q={self.anime.replace(' ', '+')}")
        Wait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "heromain")))

        soup_html = BeautifulSoup(browser.page_source, 'html.parser')
        anime_results = self._search_for_animes(
            soup_html, f"/anime/.*{self.formatted_anime}.*")
        logger.info("anime results: ")
        for anime_result in anime_results:
            logger.info(anime_result)

        if not len(anime_results):
            logger.error(
                f'Lo siento no pude encontrar el anime "{self.anime}" :(')
            browser.quit()
            exit(2)

        return anime_results, browser

    def episodes(self, selected_anime, browser):
        browser.get(f'{self.base_url}{selected_anime}')
        soup_html = BeautifulSoup(browser.page_source, 'html.parser')
        self._search_for_episodes(
            soup_html, f'/ver/.*{self.formatted_anime}.*')

    def _search_for_animes(self, soup_html, pattern):
        links = soup_html.findAll('a')
        results = []

        for link in links:
            matched_link = re.search(pattern, link['href'], re.IGNORECASE)
            if matched_link:
                results.append(matched_link.group())

        return results

    def _search_for_episodes(self, soup_html, pattern):
        links = soup_html.findAll('a')
        matched_link = ""
        list = []
        self.anime_episodes = 0
        self.episode_format = ""

        for link in links:
            try:
                matched_link = re.search(pattern, link['href'], re.IGNORECASE)
            except KeyError:
                continue

            if matched_link:
                list.append(matched_link)

        self.anime_episodes = len(list)
        split_match = matched_link.group().split('-')
        split_match.pop()
        self.episode_format = "-".join(split_match) + "-"
        logger.info(f"number of episodes {self.anime_episodes}")
        logger.info(f"episode url format {self.episode_format}")

    def select_anime(self, anime_results):
        anime_names = []
        for index in range(len(anime_results)):
            anime = anime_results[index].split('/')[2].replace('-', ' ')
            anime_names.append(anime)
            print(f'{index}) {anime}')

        try:
            selected = int(input("Elige un número: "))
        except ValueError:
            clear_screen()
            logger.warning("No escribas letras!")
            return self.select_anime(anime_results)

        try:
            return anime_results[selected], anime_names[selected]
        except IndexError:
            clear_screen()
            logger.warning(
                f"Elige un numero entre 0 y {len(anime_results) - 1}!")
            return self.select_anime(anime_results)

    def select_episode(self, browser):
        try:
            self.episode = int(
                input(f"Por favor elije un episodio entre el 1 y {self.anime_episodes}: "))
            if self.episode > self.anime_episodes:
                self.select_episode(browser)

            browser.get(f"{self.base_url}{self.episode_format}{self.episode}")

        except ValueError:
            clear_screen()
            logger.warning("No escribas letras!")
            self.select_episode(browser)

    def get_episode(self, browser):
        if self.episode > self.anime_episodes:
            self.select_episode(browser)

        browser.get(f'{self.base_url}{self.episode_format}{self.episode}')

    def get_server_link(self, browser):
        try:
            Wait(browser, 5).until(EC.visibility_of_element_located(
                (By.XPATH, f"//a[text()='{self.server}']"))).click()
        except:
            try:
                upper_server_name = self.server.capitalize()
                Wait(browser, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, f"//a[text()='{upper_server_name}']")))
            except:
                logger.error(f"No pude encontrar el servidor {self.server} :(")
                browser.quit()
                exit(2)

        link = Wait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@class='embed-responsive-item']"))).get_attribute('src')
        pattern = "https://www3?." + self.server + ".*"
        logger.info(f"pattern {pattern}")
        server_link = re.search(pattern, link).group()
        return server_link
