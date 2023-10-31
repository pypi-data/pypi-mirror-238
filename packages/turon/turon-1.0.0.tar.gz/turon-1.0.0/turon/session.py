# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin


class Session(requests.Session):
    """
    Extends requests.Session object to include `base_url` option.
    """
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        return super().request(method, urljoin(self.base_url, url), **kwargs)
