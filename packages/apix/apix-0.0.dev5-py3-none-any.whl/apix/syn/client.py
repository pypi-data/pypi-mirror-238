from ..base.client import BaseClient
from ..base.proto import Sync, ProtoHttp, ProtoPath, T
from ..serializer.base import check_response



class SyncClient(BaseClient[Sync]):
    def __call__(self, path: ProtoPath[T], **kwargs) -> T:
        request = path.build_request(self)
        resp = check_response(self.http.fetch(request))
        return path.build_result(resp, self)

    def default_http(self) -> ProtoHttp[Sync]:
        from .http.httpx_ import SyncHttpxSession

        return SyncHttpxSession()
