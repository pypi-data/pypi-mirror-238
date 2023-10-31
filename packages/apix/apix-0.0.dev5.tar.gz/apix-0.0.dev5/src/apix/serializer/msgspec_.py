import typing
import msgspec

from ..base.proto import T, ProtoSerializer, ProtoClient
from ..base.dto import PathInfo, Request, Response
from .base import build_request, build_result


class MsgspecSchema(msgspec.Struct): ...


class MsgspecPath(msgspec.Struct, typing.Generic[T]):
    __info__: typing.ClassVar[PathInfo] = PathInfo()

    def build_request(self, client: ProtoClient) -> Request:
        return build_request(self, client)
    
    def build_result(self, response: Response, client: ProtoClient) -> T:
        return build_result(self, response, client)


class MsgspecSerializer(ProtoSerializer):
    def __init__(self) -> None:
        self.__encoder = msgspec.json.Encoder()
    
    def to_json(self, obj) -> bytes:
        return self.__encoder.encode(obj)

    def from_json(self, data, type: typing.Type[T]) -> T:
        print(data, type)
        return msgspec.json.decode(data, type=type)

    def to_builtins(self, obj) -> typing.Dict[str, typing.Any]:
        return msgspec.to_builtins(obj)
