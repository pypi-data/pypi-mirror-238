import typing
import dataclasses


@dataclasses.dataclass
class Request:
    method: str
    url: str
    content: bytes = b""
    params: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Response:
    status: int
    content: bytes
    headers: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class PathInfo:
    method: str = "GET"
    path: str = "/"
    type: typing.Type = bool
