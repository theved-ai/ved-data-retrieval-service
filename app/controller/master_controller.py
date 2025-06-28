from abc import abstractmethod, ABC
from fastapi import APIRouter


class MasterController(ABC):
    router = APIRouter()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        instance = cls()
        instance._add_routes()

    @abstractmethod
    def _add_routes(self):
        pass
