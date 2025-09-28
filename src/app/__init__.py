# Copyright (c) 2024 Tony Narlock
"""Application entrypoints for HTTP and GraphQL routes."""

import strawberry
from litestar import Litestar, get
from litestar.di import Provide
from strawberry import Private
from strawberry.litestar import make_graphql_controller


@strawberry.type
class Query:
    """Root GraphQL query type."""

    greeting: Private[str] = "Hello World"

    @strawberry.field
    def hello(self) -> str:
        """Return the configured greeting.

        Returns
        -------
        str
            Greeting configured for GraphQL responses.
        """
        return self.greeting


schema = strawberry.Schema(Query)

GraphQLController = make_graphql_controller(
    schema,
    path="/graphql",
)

GraphQLController.dependencies = {
    **GraphQLController.dependencies,
    # Query construction is trivial; keep it on the loop, no worker thread needed.
    "root_value": Provide(Query, sync_to_thread=False),
}


@get(
    "/",
    # Simple string response, tell Litestar it can stay on the event loop.
    sync_to_thread=False,
)
def hello_world() -> str:
    """Return a greeting for the HTTP route.

    Returns
    -------
    str
        Plain-text greeting for the Litestar response.
    """
    return "Hello, world!"


app = Litestar(route_handlers=[hello_world, GraphQLController])
