from abc import ABC, abstractmethod


class Server(ABC):

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._set_url(url)

    def _set_url(self, url):
        self._url = url

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_video_link(self):
        pass

    @abstractmethod
    def select_quality(self):
        pass

    @abstractmethod
    def _clicks_pre_link(self):
        pass
