from ..base.proto import ProtoClient, T, ProtoPath
from ..base.dto import Response, Request



def build_request(path: ProtoPath[T], client: ProtoClient) -> Request:
    request = Request(
        method=path.__info__.method,
        url=client.build_url(path)
    )
    if path.__info__.method == "GET":
        request.params = client.config.serializer.to_builtins(path)
    else:
        request.headers["Content-Type"] = "application/json"
        request.content = client.config.serializer.to_json(path)
    return request


def build_result(path: ProtoPath[T], response: Response, client: ProtoClient) -> T:
    return client.config.serializer.from_json(response.content, path.__info__.type)


def check_response(response: Response) -> Response:
    if response.status != 200:
        raise Exception(f"Invalid response: {response}")
    return response
