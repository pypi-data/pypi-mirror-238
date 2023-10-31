import httpx

from ...base.dto import Request, Response
from .base import SyncHttp



class SyncHttpxSession(SyncHttp):
    def __init__(self) -> None:
        self.__client = httpx.Client()

    def fetch(self, request: Request) -> Response:
        resp = self.__client.request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            content=request.content
        )
        return Response(
            status=resp.status_code,
            content=resp.content,
        )
