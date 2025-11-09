from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Todo as TodoModel
from typing import List

# Создание таблиц при запуске приложения (только для демонстрации)
# В реальном проекте используйте миграции (alembic)
TodoModel.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "To-Do API - CI/CD Demo"}

@app.post("/todos/", response_model=dict)
def create_todo(title: str, description: str = None, completed: bool = False, db: Session = Depends(get_db)):
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    
    todo = TodoModel(title=title, description=description, completed=completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed}

@app.get("/todos/", response_model=List[dict])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = db.query(TodoModel).offset(skip).limit(limit).all()
    return [{"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed} for todo in todos]

@app.put("/todos/{todo_id}", response_model=dict)
def update_todo(todo_id: int, title: str = None, description: str = None, completed: bool = None, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if completed is not None:
        todo.completed = completed
    
    db.commit()
    db.refresh(todo)
    return {"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}