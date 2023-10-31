from attrs import define
from collections.abc import Callable
from typing import TypeAlias, Any, Iterable, TypedDict, Literal
from incant import Incanter


@define
class Request:
    pass


@define
class Response:
    body: bytes  # The response body


WhiscantHandler: TypeAlias = Callable[[Request], Response]


def hello(request: Request) -> Response:
    return Response(b"Hello world!")


def post_request(request: Request) -> Response:
    return Response(b"Successful request.")


HttpMethod: TypeAlias = Literal["GET", "POST"]
HttpRoute: TypeAlias = str


class Environ(TypedDict):
    REQUEST_METHOD: HttpMethod
    PATH_INFO: HttpRoute


StartResponseCallable: TypeAlias = Callable[[str, list[tuple[str, str]], Any], None]
WSGICallable: TypeAlias = Callable[[Environ, StartResponseCallable], Iterable[bytes]]


def whiscant(
    handlers: list[tuple[HttpRoute, HttpMethod, WhiscantHandler]],
    customizer: Callable[[Incanter], None] = lambda _: None,
) -> WSGICallable:
    incanter = Incanter()

    def not_found_handler(request: Request) -> Response:
        return Response(b"Not Found")

    incanter.register_by_name(lambda: not_found_handler)

    routes = {(path, method): handler for path, method, handler in handlers}

    @incanter.register_by_name(name="handler")
    def router(environ: Environ, not_found_handler: WhiscantHandler) -> WhiscantHandler:
        """The handler router."""

        return routes.get(
            (environ["PATH_INFO"], environ["REQUEST_METHOD"]), not_found_handler
        )

    customizer(incanter)

    def call_handler(
        handler: WhiscantHandler, start_response: StartResponseCallable
    ) -> Iterable[bytes]:
        start_response("200 OK", [], None)
        return [handler(Request()).body]

    return incanter.compose(call_handler)


def our_customizer(incanter: Incanter) -> None:
    def custom_not_found_handler(request: Request) -> Response:
        return Response(b"Custom not found!")

    incanter.register_by_name(
        lambda: custom_not_found_handler, name="not_found_handler"
    )


app = whiscant([("/", "GET", hello), ("/", "POST", post_request)], our_customizer)
from inspect import getsource

print(getsource(app))
