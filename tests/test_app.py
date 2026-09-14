import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def reset_tasks():
    tasks.clear()

    tasks.extend([
        {
            "id": 1,
            "title": "Complete Docker assignment",
            "completed": False
        },
        {
            "id": 2,
            "title": "Test GitHub Actions",
            "completed": False
        }
    ])


def test_home_page(client):
    reset_tasks()

    response = client.get("/")

    assert response.status_code == 200
    assert b"TaskFlow" in response.data


def test_add_task(client):
    reset_tasks()

    response = client.post(
        "/add",
        data={"title": "Learn Docker"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert any(
        task["title"] == "Learn Docker"
        for task in tasks
    )


def test_complete_task(client):
    reset_tasks()

    response = client.post(
        "/complete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert tasks[0]["completed"] is True


def test_delete_task(client):
    reset_tasks()

    response = client.post(
        "/delete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert not any(
        task["id"] == 1
        for task in tasks
    )


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"