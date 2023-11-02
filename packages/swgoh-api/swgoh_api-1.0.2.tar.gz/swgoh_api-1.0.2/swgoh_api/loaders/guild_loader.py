from .base_local_loader import BaseLocalLoader
from .base_remote_loader import BaseRemoteLoader
from ..utils.singleton import singleton
from ..url_requests.url_request import GuildURLRequest
from ..entities.guild import Guild


@singleton
class GuildRemoteLoader(BaseRemoteLoader):
    def __init__(self):
        super().__init__()
        self._request_cls = GuildURLRequest

    def load(self, *args):
        res = super().load(*args)
        if res:
            res = Guild(res, use_cache=False)
        return res


@singleton
class GuildLocalLoader(BaseLocalLoader):
    def __init__(self):
        super().__init__()
        self._obj_cls = Guild

    def _get_path(self, path, name):
        return f"{path}/{name}/data.json"

    def load(self, *args):
        data = self._read_data(*args)
        if data:
            return Guild(data, load_path=args[0])
        return None
