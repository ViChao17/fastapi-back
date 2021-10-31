import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from add_review_from_csv import set_review
from threading import Thread
from typing import Optional
import json


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/testitem/")
def test_item(item: str, db: Session = Depends(get_db)):
    item_out_python = json.JSONDecoder().decode(item)
    type_chart = item_out_python['type']
    return {'type': type_chart}


@app.get("/region/")
def region(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_review_by_region(db=db, region=filters_dict.get('region', []),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/subregion/")
def subregion(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_review_by_subregion(db=db, subregion=filters_dict.get('subregion', []),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/var/")
def var(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_world_review_by_var(db=db, year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/int_org/")
def int_org(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_review_by_int_org(db=db, int_org=filters_dict.get('int_org', []),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/country/")
def country(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_review_by_country(db=db, country=filters_dict.get('country', []),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


def set_to_stat(rule: dict, item_set: List[schemas.Review]):
    type_chart: str | None = rule.get('type')
    x_field = rule.get('x_field')

    series = [{
        'type': 'line',
        'data': [
            {
                'x': 0,
                'y': 0
            },
            {
                'x': 1,
                'y': 2
            }
        ]
    }]

    if type_chart:
        series[0]['name'] = x_field
        series[0]['type'] = type_chart
        stat_data: list = []
        data_set = param_value(x_field, item_set)
        for key in data_set:
            stat_data.append(
                {
                    'x': key,
                    'y': data_set[key]
                }
            )
        series[0]['data'] = stat_data
    else:
        series[0]['name'] = 'Error'
#
    return series


def param_value(param: str, item_set: List[schemas.Review]):    # param = Year | Var
    data_set = {}
    for item in item_set:
        data_set[getattr(item, param)] = data_set.get(getattr(item, param), 0) + item.Value
    return data_set


# @app.get("/review/")
# def add_review(db: Session = Depends(get_db)):
#     thread = Thread(target=set_review, args=(db, ))
#     thread.start()
#     thread.join()
#     return {'status': 'OK'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
