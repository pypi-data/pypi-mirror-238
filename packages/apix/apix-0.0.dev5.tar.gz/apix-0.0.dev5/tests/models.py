from apix.serializer.msgspec_ import MsgspecPath, MsgspecSchema
from apix.base.dto import PathInfo

class Data(MsgspecSchema):
    key: str
    value: str


class GetData(MsgspecPath[Data]):
    __info__ = PathInfo("GET", "/data", Data)

    key: str


class PostData(MsgspecPath[bool]):
    __info__ = PathInfo("POST", "/data", bool)

    key: str
    value: str
