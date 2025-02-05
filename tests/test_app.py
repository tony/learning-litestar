from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient

from app import app

app.debug = True


def test_hello_world() -> None:
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK
        assert response.text == "Hello, world!"


def test_graphql_hello() -> None:
    with TestClient(app=app) as client:
        response = client.post(
            "/graphql",
            json={
                "query": r"""
query {
  hello
}"""
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.json() == {
            "data": {
                "hello": "Hello World",
            },
        }
