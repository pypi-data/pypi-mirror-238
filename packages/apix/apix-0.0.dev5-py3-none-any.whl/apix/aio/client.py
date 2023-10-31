from ..base.client import BaseClient
from ..base.proto import Async, ProtoHttp, ProtoPath, T
from ..serializer.base import check_response



class AsyncClient(BaseClient[Async]):
    async def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = path.build_request(self)
        resp = check_response(await self.http.fetch(request))
        return path.build_result(resp, self)

    def default_http(self) -> ProtoHttp[Async]:
        from .http.httpx_ import AsyncHttpxSession

        return AsyncHttpxSession()
