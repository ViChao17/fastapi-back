from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from . import models, schemas

from typing import Optional


def get_review(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()


def get_review_by_var(db: Session, skip: int = 0, limit: int = 100, var: str = ''):
    return db.query(models.Review).filter(models.Review.Var == var).offset(skip).limit(limit).all()


params = ['Country', 'Year', 'Region', 'SubRegion', 'OPEC', 'EU', 'OECD', 'CIS', 'Var', 'Value']


def get_full_review_by_region(db: Session, region: list, year: Optional[dict] = None, var: Optional[list] = None):
    items: Query = db.query(models.Review).filter(models.Review.Region.in_(region))
    if year:
        items = year_comparison_review(items, year)
    if var:
        items = items.filter(models.Review.Var.in_(var))
    return items.all()


def get_full_review_by_subregion(db: Session, subregion: list, year: Optional[dict] = None, var: Optional[list] = None):
    items: Query = db.query(models.Review).filter(models.Review.SubRegion.in_(subregion))
    if year:
        items = year_comparison_review(items, year)
    if var:
        items = items.filter(models.Review.Var.in_(var))
    return items.all()


def get_full_review_by_int_org(db: Session, int_org: dict, year: Optional[dict] = None, var: Optional[list] = None):
    items: Query = db.query(models.Review).filter(in_org(int_org))
    if year:
        items = year_comparison_review(items, year)
    if var:
        items = items.filter(models.Review.Var.in_(var))
    return items.all()


def get_full_world_review_by_var(db: Session, var: list, year: Optional[dict] = None):
    items: Query = db.query(models.Review).filter(models.Review.Var.in_(var))
    if year:
        items = year_comparison_review(items, year)
    return items


def get_full_review_by_country(db: Session, country: list, year: Optional[dict] = None, var: Optional[list] = None):
    items: Query = db.query(models.Review).filter(models.Review.Country.in_(country))
    if year:
        items = year_comparison_review(items, year)
    if var:
        items = items.filter(models.Review.Var.in_(var))
    return items.all()


def year_comparison_review(items: Query, year: dict) -> Query:
    current_year = int(list(year.keys())[0])
    condition = year[str(current_year)]
    if condition == 'more':
        return items.filter(models.Review.Year > current_year)
    if condition == 'less':
        return items.filter(models.Review.Year < current_year)
    if condition == 'equal':
        return items.filter(models.Review.Year == current_year)
    if condition == 'more_or_equal':
        return items.filter(models.Review.Year >= current_year)
    if condition == 'less_or_equal':
        return items.filter(models.Review.Year <= current_year)
    return items


def in_org(int_org: dict) -> bool:
    for key in int_org.keys():
        if key == 'CIS' and models.Review.CIS and int_org[key]:
            return True
        if key == 'EU' and models.Review.EU and int_org[key]:
            return True
        if key == 'OECD' and models.Review.OECD and int_org[key]:
            return True
        if key == 'OPEC' and models.Review.OPEC and int_org[key]:
            return True
    return False
