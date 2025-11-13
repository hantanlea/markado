# from fastapi import FastAPI
# from fastapi.testclient import TestClient


def test_smoke():
    assert 1 + 1 == 2


# app = FastAPI()


# @app.get("/")
# async def read_main():
# return {"msg": "Hello World"}

# client = TestClient(app)

# def test_read_main():
# response = client.get("/")
# assert response.status_code == 200
# assert response.json() == {"msg": "Hello World"}
