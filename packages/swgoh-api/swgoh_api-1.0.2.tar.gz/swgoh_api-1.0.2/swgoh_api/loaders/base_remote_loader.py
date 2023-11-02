from .base_loader import BaseLoader
from ..url_requests.requester import Requester


class BaseRemoteLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self._requester = Requester()
        self._request_cls = None

    def load(self, *args):
        if self._request_cls:
            request = self._request_cls(*args)
            return self._requester.make_request(request)
        return None
