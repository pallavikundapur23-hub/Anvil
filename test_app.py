from app import app

client = app.test_client()


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200


def test_add_task():

    response = client.post(
        "/tasks",
        json={
            "title": "Test task"
        }
    )

    assert response.status_code == 201