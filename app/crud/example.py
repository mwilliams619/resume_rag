from sqlalchemy.orm import Session
from app.models.example import ExampleModel
from app.schemas.example import ExampleCreate, ExampleUpdate

def create_example(db: Session, example: ExampleCreate):
    db_example = ExampleModel(**example.dict())
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example

def get_example(db: Session, example_id: int):
    return db.query(ExampleModel).filter(ExampleModel.id == example_id).first()

def get_examples(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ExampleModel).offset(skip).limit(limit).all()

def update_example(db: Session, example_id: int, example: ExampleUpdate):
    db_example = db.query(ExampleModel).filter(ExampleModel.id == example_id).first()
    if db_example:
        for key, value in example.dict(exclude_unset=True).items():
            setattr(db_example, key, value)
        db.commit()
        db.refresh(db_example)
    return db_example

def delete_example(db: Session, example_id: int):
    db_example = db.query(ExampleModel).filter(ExampleModel.id == example_id).first()
    if db_example:
        db.delete(db_example)
        db.commit()
    return db_example