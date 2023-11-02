import ujson as json
from .base_loader import BaseLoader


class BaseLocalLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self._obj_cls = None

    def load(self, *args):
        if self._obj_cls:
            data = self._read_data(*args)
            if data:
                return self._obj_cls(data)
        return None

    def _read_data(self, path, name):
        res = None
        data_path = self._get_path(path, name)
        if not data_path:
            return None
        try:
            with open(data_path, "r") as f:
                res = json.load(f)
        except Exception:
            pass
        return res

    def _get_path(self, path, name):
        return None

