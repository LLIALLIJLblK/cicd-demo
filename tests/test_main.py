import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Todo as TodoModel

client = TestClient(app)

def test_read_root():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert "To-Do API" in response.json()["message"]

def test_create_todo(db_session):
    """Тест создания задачи"""
    response = client.post("/todos/", params={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    assert "id" in data

def test_create_todo_without_title(db_session):
    """Тест создания задачи без заголовка (должна быть ошибка)"""
    response = client.post("/todos/", params={"title": "", "description": "Test Description"})
    assert response.status_code == 400

def test_read_todos(db_session):
    """Тест получения списка задач"""
    # Сначала создадим задачи
    client.post("/todos/", params={"title": "Todo 1", "description": "Description 1"})
    client.post("/todos/", params={"title": "Todo 2", "description": "Description 2"})
    
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert any(todo["title"] == "Todo 1" for todo in data)
    assert any(todo["title"] == "Todo 2" for todo in data)

def test_update_todo(db_session):
    """Тест обновления задачи"""
    # Создаем задачу
    create_response = client.post("/todos/", params={"title": "Original Title", "description": "Original Description"})
    assert create_response.status_code == 200
    created_data = create_response.json()
    
    # Обновляем задачу
    update_response = client.put(f"/todos/{created_data['id']}", params={
        "title": "Updated Title",
        "completed": "true"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Title"
    assert updated_data["completed"] == True

def test_delete_todo(db_session):
    """Тест удаления задачи"""
    # Создаем задачу
    create_response = client.post("/todos/", params={"title": "To Delete", "description": "To Delete Description"})
    assert create_response.status_code == 200
    created_data = create_response.json()
    
    # Удаляем задачу
    delete_response = client.delete(f"/todos/{created_data['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Todo deleted successfully"
    
    # Проверяем, что задача удалена
    get_response = client.get(f"/todos/")
    assert created_data['id'] not in [todo['id'] for todo in get_response.json()]