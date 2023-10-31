import typing
from .proto import OP, ProtoHttp, ProtoSerializer, ProtoConfig
from ..serializer.default import default_serializer
import dataclasses


@dataclasses.dataclass
class ClientConfig(ProtoConfig[OP]):
    base_url: str = "https://api.example.com"
    serializer: ProtoSerializer = dataclasses.field(
        default_factory=default_serializer)
    http: typing.Optional[ProtoHttp[OP]] = None
