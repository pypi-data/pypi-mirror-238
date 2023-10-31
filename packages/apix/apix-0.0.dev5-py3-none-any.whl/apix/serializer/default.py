from ..base.proto import ProtoSerializer


def default_serializer() -> ProtoSerializer:
    from .msgspec_ import MsgspecSerializer

    return MsgspecSerializer()
