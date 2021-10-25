from sql_app import models
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Depends
import csv

models.Base.metadata.create_all(bind=engine)
item_type = ['Country', 'Year', 'ISO3166_alpha3', 'ISO3166_numeric', 'Region', 'SubRegion', 'OPEC', 'EU', 'OECD', 'CIS', 'Var', 'Value']


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_item(db: Session, item):
    db_item = models.Review(Country=str(item[0]), Year=int(item[1]), Region=str(item[4]), SubRegion=str(item[5]),
                            OPEC=bool(int(item[6])), EU=bool(int(item[7])), OECD=bool(int(item[8])), CIS=bool(int(item[9])),
                            Var=str(item[10]), Value=float(item[11]))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


def set_review(db: Session):
    with open("bp-stats-review-2021-consolidated-dataset-narrow-format.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        en = enumerate(reader)
        print(en.__next__())
        for i, item in en:
            if i % 1000 == 0:
                print(f'{i/2520}%')
            add_item(db, item)
        print('--End--')


if __name__ == '__main__':
    set_review(Depends(get_db))
