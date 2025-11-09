from app.models import Todo as TodoModel
from sqlalchemy.orm import Session

def test_todo_model_creation(db_session: Session):
    """Тест создания модели Todo в БД"""
    todo = TodoModel(title="Test Todo", description="Test Description", completed=False)
    db_session.add(todo)
    db_session.commit()
    
    retrieved_todo = db_session.query(TodoModel).filter(TodoModel.title == "Test Todo").first()
    assert retrieved_todo is not None
    assert retrieved_todo.title == "Test Todo"
    assert retrieved_todo.description == "Test Description"
    assert retrieved_todo.completed == False

def test_todo_model_defaults(db_session: Session):
    """Тест значений по умолчанию для модели Todo"""
    todo = TodoModel(title="Test Without Description")
    db_session.add(todo)
    db_session.commit()
    
    retrieved_todo = db_session.query(TodoModel).filter(TodoModel.title == "Test Without Description").first()
    assert retrieved_todo is not None
    assert retrieved_todo.title == "Test Without Description"
    assert retrieved_todo.description is None
    assert retrieved_todo.completed == False