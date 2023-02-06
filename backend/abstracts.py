import abc
from abc import ABC
from contextlib import contextmanager

from sqlmodel import SQLModel


class BaseClient(ABC):

    @contextmanager
    @abc.abstractmethod
    def get_session(self):
        pass


class BaseService(ABC):
    client = BaseClient
    model = None

    @abc.abstractmethod
    def all(self) -> list[SQLModel]:
        pass
