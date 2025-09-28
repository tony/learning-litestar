# Copyright (c) 2024 Tony Narlock
"""Application entrypoints for HTTP and GraphQL routes."""

from typing import ClassVar

import strawberry
from litestar import Litestar, get
from strawberry.litestar import make_graphql_controller


@strawberry.type
class Query:
    """Root GraphQL query type."""

    _GREETING: ClassVar[str] = "Hello World"

    @strawberry.field
    def hello(self) -> str:
        """Return the configured greeting.

        Returns
        -------
        str
            Greeting configured for GraphQL responses.
        """
        return self._GREETING


schema = strawberry.Schema(Query)

GraphQLController = make_graphql_controller(
    schema,
    path="/graphql",
)


@get("/")
def hello_world() -> str:
    """Return a greeting for the HTTP route.

    Returns
    -------
    str
        Plain-text greeting for the Litestar response.
    """
    return "Hello, world!"


app = Litestar(route_handlers=[hello_world, GraphQLController])
