import requests as rq
from requests.exceptions import HTTPError
from .url_request import *
from ..utils.singleton import singleton


@singleton
class Requester(object):
    def make_request(self, req, **kwargs):
        try:
            resp = rq.get(req.url, kwargs)
            resp.raise_for_status()
        except HTTPError as err:
            pass
        except Exception as err:
            pass
        else:
            return req.handle_data(resp, self)
        req.error()

    def _make_stream_request(self, req):
        return self.make_request(req, stream=True)
