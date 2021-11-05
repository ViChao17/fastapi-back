from sql_app import models
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
import csv

item_type = ['Country', 'Year', 'ISO3166_alpha3', 'ISO3166_numeric', 'Region', 'SubRegion', 'OPEC', 'EU', 'OECD', 'CIS', 'Var', 'Value']


def add_item(db: Session, item):
    db_item = models.Review(Country=str(item[0]), Year=int(str(item[1])), Region=str(item[4]), SubRegion=str(item[5]),
                            OPEC=bool(int(item[6])), EU=bool(int(item[7])), OECD=bool(int(item[8])), CIS=bool(int(item[9])),
                            Var=str(item[10]), Value=float(item[11]))
    db.add(db_item)


def set_review(db: Session):
    with open("bp-stats-review-2021-consolidated-dataset-narrow-format.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        en = enumerate(reader)
        print('start!')
        en.__next__()
        for i, item in en:
            if i % 1000 == 0:
                print(f'{i/2520}%')
            try:
                add_item(db=db, item=item)
            except:
                pass
        print('commit ...')
        db.commit()
        print('--End--')


if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    s = SessionLocal()
    set_review(s)
    print('Data base created!')
