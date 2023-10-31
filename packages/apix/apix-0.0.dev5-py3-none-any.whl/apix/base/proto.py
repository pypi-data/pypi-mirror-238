from __future__ import annotations

import typing

from .dto import PathInfo, Request, Response


class Operation: ...
class Sync(Operation): ...
class Async(Operation): ...

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)
OP = typing.TypeVar("OP")
OP_co = typing.TypeVar("OP_co", covariant=True)


class ProtoSerializer(typing.Protocol):
    def to_json(self, obj: typing.Any) -> bytes: ...
    def from_json(self, data: bytes, type: typing.Type[T]) -> T: ...
    def to_builtins(self, obj: typing.Any) -> typing.Dict[str, typing.Any]: ...


class ProtoSchema(typing.Protocol): ...


class ProtoPath(typing.Protocol[T_co]):
    __info__: typing.ClassVar[PathInfo]

    def build_request(self, client: ProtoClient) -> Request: ...
    def build_result(self, response: Response, client: ProtoClient) -> T_co: ...


class ProtoHttp(typing.Protocol[OP_co]):
    @typing.overload
    def fetch(self: ProtoHttp[Sync], request: Request) -> Response: ...

    @typing.overload
    async def fetch(self: ProtoHttp[Async], request: Request) -> Response: ...


class ProtoConfig(typing.Protocol[OP]):
    base_url: str
    serializer: ProtoSerializer
    http: typing.Optional[ProtoHttp[OP]]


class ProtoClient(typing.Protocol[OP_co]):
    @typing.overload
    def __call__(self: ProtoClient[Sync], path: ProtoPath[T], **kwargs) -> T: ...

    @typing.overload
    async def __call__(self: ProtoClient[Async], path: ProtoPath[T], **kwargs) -> T: ...

    @property
    def config(self) -> ProtoConfig[OP_co]: ...

    @property
    def http(self) -> ProtoHttp: ...

    def default_http(self) -> ProtoHttp[OP_co]: ...
    def build_url(self, path: ProtoPath[T]) -> str: ...
