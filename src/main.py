from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.base import Base
from src.db.session import engine



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Запуск приложения")
    yield    
    print("Выключение приложения")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,     # Позволяет передавать куки и заголовки авторизации
    allow_methods=["*"],        # Разрешает все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],        # РАЗРЕШАЕТ ЗАГОЛОВКИ (исправляет ошибку 400 OPTIONS)
)




def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)


def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.name)

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(payload: Task_Create, db: Session = Depends(get_db)) -> TaskSchema: 
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed
    
    db.commit()
    return task_for_update
        
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()



 
@app.get("/categories")
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in categories_from_db]


@app.post("/categories", status_code=201)
def create_categories(payload: Create_and_Update_Category, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()
    return category_orm_to_model(new_category)

@app.patch("/categories/{id}")
def update_category(id: str, payload: Create_and_Update_Category, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, id)
    if payload.name:
        category_for_update.name = payload.name
    if category_for_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    db.commit()
    return category_for_update

@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: str, db: Session = Depends(get_db)) -> None:
    category_for_delete = db.get(CategoryORM, id)
    if category_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db.delete(category_for_delete)
    db.commit()
# Тестовый комментарий для Pull Request
