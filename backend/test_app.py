from app import app


def test_health_is_ok():
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_tasks_returns_a_list():
    client = app.test_client()
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_task_works():
    client = app.test_client()
    response = client.post("/api/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Write tests"


def test_add_task_without_title_is_rejected():
    client = app.test_client()
    response = client.post("/api/tasks", json={"title": "     "})
    assert response.status_code == 400
