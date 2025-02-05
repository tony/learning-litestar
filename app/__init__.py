import strawberry
from litestar import Litestar, get
from strawberry.litestar import make_graphql_controller


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

GraphQLController = make_graphql_controller(
    schema,
    path="/graphql",
)


@get("/")
async def hello_world() -> str:
    return "Hello, world!"


app = Litestar(route_handlers=[hello_world, GraphQLController])
