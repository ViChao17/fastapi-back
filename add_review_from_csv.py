from sql_app import models
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends
import csv

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_item(db: Session, item):
    pass


def set_review(db: Session):
    with open("bp-stats-review-2021-consolidated-dataset-narrow-format.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        en = enumerate(reader)
        print(en.__next__())


if __name__ == '__main__':
    set_review(Depends(get_db))
