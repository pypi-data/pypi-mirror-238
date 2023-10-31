from abc import ABC, abstractmethod
from contextlib import contextmanager

import requests


class AzureClientCredentialsABC(ABC):
    """
    Abstract class for Azure credentials. Two methods must be implemented:
    - get_token to return a token
    - session: a context manager to use for sending requests.
    """

    @abstractmethod
    def get_token(self) -> str:
        pass

    @abstractmethod
    @contextmanager
    def session(self) -> requests.Session:
        pass
