from abc import ABC, abstractmethod, abstractproperty


class Site(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def episodes(self):
        pass

    @abstractmethod
    def _search_for_animes(self):
        pass

    @abstractmethod
    def _search_for_episodes(self):
        pass

    @abstractmethod
    def select_anime(self):
        pass

    @abstractmethod
    def select_episode(self):
        pass

    @abstractmethod
    def get_episode(self):
        pass

    @abstractmethod
    def get_server_link(self):
        pass

    @abstractproperty
    def base_url(self):
        pass

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._set_server(server)

    def _set_server(self, server):
        self._server = server

    @property
    def anime(self):
        return self._anime

    @anime.setter
    def anime(self, anime):
        self._set_anime(anime)

    def _set_anime(self, anime):
        self._anime = anime

    @property
    def episode(self):
        return self._episode

    @episode.setter
    def episode(self, episode):
        self._set_episode(episode)

    def _set_episode(self, episode):
        self._episode = episode
