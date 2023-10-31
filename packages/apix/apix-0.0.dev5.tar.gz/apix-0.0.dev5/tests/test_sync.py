import httpx
import apix
from apix.syn.client import SyncClient
import pytest
import typing
from .models import Data, GetData, PostData

T = typing.TypeVar("T")


class MySyncClient(SyncClient):
    def get_data(self, key: str) -> Data:
        return self(GetData(key))

    def post_data(self, key: str, value: str) -> bool:
        return self(PostData(key, value))

@pytest.fixture
def client():
    return MySyncClient()


@pytest.mark.respx(base_url="https://api.example.com")
def test_def(respx_mock, client):
    mocked = respx_mock.get("/").mock(return_value=httpx.Response(200, json=True))
    result = client(apix.serializer.msgspec_.MsgspecPath[bool]())
    assert mocked.called
    assert result


@pytest.mark.respx(base_url="https://api.example.com")
def test_get_data(respx_mock, client):
    tested_data = Data("foo", "fooson")

    mocked = respx_mock.get("/data", params={"key": "foo"}).mock(
        return_value=httpx.Response(
            status_code=200, 
            headers={"Content-Type": "application/json"},
            content=client.config.serializer.to_json(tested_data)
        )
    )
    result = client.get_data("foo")
    assert mocked.called
    assert tested_data == result
