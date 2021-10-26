from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from . import models, schemas

from typing import Optional


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_review(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()


def get_review_by_var(db: Session, skip: int = 0, limit: int = 100, var: str = ''):
    return db.query(models.Review).filter(models.Review.Var == var).offset(skip).limit(limit).all()


params = ['Country', 'Year', 'Region', 'SubRegion', 'OPEC', 'EU', 'OECD', 'CIS', 'Var', 'Value']


def get_full_review_by_region(db: Session, region: list, year: Optional[dict] = None, var: Optional[list] = None):
    pass


def get_full_review_by_subregion(db: Session, subregion: list, year: Optional[dict] = None, var: Optional[list] = None):
    pass


def get_full_review_by_int_org(db: Session, int_org: dict, year: Optional[dict] = None, var: Optional[list] = None):
    pass


def get_full_world_review_by_var(db: Session, var: list, year: Optional[dict] = None):
    pass


def get_full_review_by_country(db: Session, country: list, year: Optional[dict] = None, var: Optional[list] = None):
    items: Query = db.query(models.Review).filter(models.Review.Country == 'Algeria')
    items = items.filter(models.Review.Year == 1973)
    items = items.filter(models.Review.Var == 'co2_mtco2')
    return items.all()

