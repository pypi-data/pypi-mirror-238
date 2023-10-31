import typing
from .proto import ProtoClient, OP, ProtoConfig, ProtoHttp, ProtoPath, T

from .config import ClientConfig




class BaseClient(ProtoClient[OP]):
    def __init__(
            self, 
            config: typing.Optional[ProtoConfig] = None
    ) -> None:
        self._http: typing.Optional[ProtoHttp[OP]]
        self._config = config or ClientConfig()
        if self._config.http is None:
            self._http = self.default_http()
        else:
            self._http = None

    @property
    def config(self) -> ProtoConfig:
        return self._config
    
    @property
    def http(self) -> ProtoHttp[OP]:
        if _http := self._http or self.config.http:
            return _http
        raise RuntimeError("Client is not initialized http")

    def build_url(self, path: ProtoPath[T]) -> str:
        return self.config.base_url + path.__info__.path