from .base_remote_loader import BaseRemoteLoader
from ..utils.singleton import singleton
from ..url_requests.url_request import UnitURLRequest
from ..entities.player import Unit


@singleton
class UnitRemoteLoader(BaseRemoteLoader):
    def __init__(self):
        super().__init__()
        self._request_cls = UnitURLRequest

    def load(self, *args):
        res = super().load(*args)
        if res:
            res = Unit(res)
        return res
