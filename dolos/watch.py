from subprocess import run, PIPE

from dolos.sites import ANIME_SITES
from dolos.servers.fembed import Fembed
from dolos.util import logger


def watch_anime(anime, episode, anime_site="animeflv", server="fembed"):
    site = ANIME_SITES[anime_site]
    site.setup(anime, episode, server)

    anime_results, browser = site.search()
    selected_anime, title = site.select_anime(anime_results)

    logger.info(f"selected anime {selected_anime}")
    logger.info(f"searched anime {anime}")

    site.episodes(selected_anime, browser)
    site.get_episode(browser)

    server_link = site.get_server_link(browser)
    server = Fembed(server_link)
    video_link = server.get_video_link(browser)
    logger.info(f"video link {video_link}")

    browser.quit()
    logger.debug("Closed all browser's tabs")

    run(['mpv', video_link,
        f"--title={title} episodio {site.episode}"], stdout=PIPE, stderr=PIPE)
