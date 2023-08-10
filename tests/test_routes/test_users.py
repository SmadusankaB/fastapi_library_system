import json


def test_create_user(client):
    data = {
        "username": "testdeveloper",
        "email": "test@user.com",
        "password": "testdeveloper",
    }
    response = client.post("/users/", data=json.dumps(data))
    assert response.status_code == 405
