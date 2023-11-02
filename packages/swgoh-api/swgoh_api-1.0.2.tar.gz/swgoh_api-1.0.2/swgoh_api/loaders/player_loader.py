from .base_local_loader import BaseLocalLoader
from .base_remote_loader import BaseRemoteLoader
from ..utils.singleton import singleton
from ..url_requests.url_request import PlayerURLRequest
from ..entities.player import Player


@singleton
class PlayerRemoteLoader(BaseRemoteLoader):
    def __init__(self):
        super().__init__()
        self._request_cls = PlayerURLRequest

    def load(self, *args):
        res = super().load(*args)
        if res:
            res = Player(res)
        return res


@singleton
class PlayerLocalLoader(BaseLocalLoader):
    def __init__(self):
        super().__init__()
        self._obj_cls = Player

    def _get_path(self, path, name):
        return f"{path}/{name}.json"
