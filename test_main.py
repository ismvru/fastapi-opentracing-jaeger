from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello():
    with client.get("/") as req:
        assert req.json() == {"Hello": "World"}
