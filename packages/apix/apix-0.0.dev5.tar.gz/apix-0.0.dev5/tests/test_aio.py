import httpx
import pytest_asyncio
import apix
from apix.aio.client import AsyncClient
import pytest
import typing
from .models import Data, GetData, PostData

T = typing.TypeVar("T")

pytestmark = pytest.mark.asyncio


class MyAsyncClient(AsyncClient):
    async def get_data(self, key: str) -> Data:
        return await self(GetData(key))

    async def post_data(self, key: str, value: str) -> bool:
        return await self(PostData(key, value))


@pytest_asyncio.fixture
async def client():
    return MyAsyncClient()


@pytest.mark.respx(base_url="https://api.example.com")
async def test_def(respx_mock, client):
    mocked = respx_mock.get("/").mock(return_value=httpx.Response(200, json=True))
    result = await client(apix.serializer.msgspec_.MsgspecPath[bool]())
    assert mocked.called
    assert result


@pytest.mark.respx(base_url="https://api.example.com")
async def test_get_data(respx_mock, client):
    tested_data = Data("foo", "fooson")

    mocked = respx_mock.get("/data", params={"key": "foo"}).mock(
        return_value=httpx.Response(
            status_code=200, 
            headers={"Content-Type": "application/json"},
            content=client.config.serializer.to_json(tested_data)
        )
    )
    result = await client.get_data("foo")
    assert mocked.called
    assert tested_data == result
