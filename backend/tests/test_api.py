from fastapi.testclient import TestClient

from markado.app import app


def test_smoke():
    assert 1 + 1 == 2


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# app = FastAPI()


# @app.get("/")
# async def read_main():
# return {"msg": "Hello World"}

# def test_read_main():
# response = client.get("/")
# assert response.status_code == 200
# assert response.json() == {"msg": "Hello World"}
