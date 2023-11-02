from .base_remote_loader import BaseRemoteLoader
from ..utils.singleton import singleton
from ..url_requests.url_request import ImageURLRequest


@singleton
class ImageRemoteLoader(BaseRemoteLoader):
    def __init__(self):
        super().__init__()
        self._request_cls = ImageURLRequest
