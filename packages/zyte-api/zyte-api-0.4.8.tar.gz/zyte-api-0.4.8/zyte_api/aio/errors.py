# -*- coding: utf-8 -*-
import logging

from aiohttp import ClientResponseError

from zyte_api.errors import ParsedError

logger = logging.getLogger(__name__)


class RequestError(ClientResponseError):
    """ Exception which is raised when Request-level error is returned.
    In contrast with ClientResponseError, it allows to inspect response
    content.
    """
    def __init__(self, *args, **kwargs):
        self.response_content = kwargs.pop("response_content")
        self.request_id = kwargs.pop("request_id", None)
        if self.request_id is None:
            self.request_id = kwargs.get("headers", {}).get("request-id")
        super().__init__(*args, **kwargs)

    @property
    def parsed(self):
        return ParsedError.from_body(self.response_content)

    def __str__(self):
        return f"RequestError: {self.status}, message={self.message}, " \
               f"headers={self.headers}, body={self.response_content}, " \
               f"request_id={self.request_id}"
