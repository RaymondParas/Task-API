from sqlalchemy.orm import Session
from . import models, schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()

def create_task(db: Session, task: schemas.Task):
    print('Task to be created', task)
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, id: int):
    db_task = get_task_by_id(db=db, id=id)
    if db_task is None:
        return None

    print('Task to be deleted', db_task)
    db.delete(db_task)
    db.commit()
    return db_task