from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/")
def read_root():
    return """TASK API"""

@app.get("/Tasks/all", response_model=List[schemas.Task])
def get_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@app.get("/Tasks/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db=db, id=id)
    if task is None:
      raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.post("/Tasks/create", response_model=schemas.Task)
def create_task(task: schemas.Task, db: Session = Depends(get_db)):
    if task.id:
      db_task = crud.get_task_by_id(db=db, id=task.id)
      if db_task:
        raise HTTPException(status_code=400, detail="Task ID already exists")

    if not task.description or task.description.isspace():
      task.description = None

    return crud.create_task(db=db, task=task)

@app.delete("/Tasks/{id}", response_model=schemas.Task)
def delete_task(id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db=db, id=id)
    if deleted_task is None:
      raise HTTPException(status_code=404, detail="Task not found")

    return deleted_task