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
    items = crud.get_full_review_by_int_org(db=db, int_org=filters_dict.get('int_org', {}),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/country/")
def country(rule: str, filters: Optional[str] = '', db: Session = Depends(get_db)):
    filters_dict: dict = json.JSONDecoder().decode(filters)
    items = crud.get_full_review_by_country(db=db, country=filters_dict.get('country', []),
                                            year=filters_dict.get('year'), var=filters_dict.get('var'))
    return set_to_stat(json.JSONDecoder().decode(rule), items)


@app.get("/variables/")
def variables(db: Session = Depends(get_db)):
    return crud.get_all_var(db)


@app.get("/all_country/")
def all_country(db: Session = Depends(get_db)):
    return crud.get_all_country(db)


@app.get("/all_region/")
def all_region(db: Session = Depends(get_db)):
    return crud.get_all_region(db)


@app.get("/all_subregion/")
def all_subregion(db: Session = Depends(get_db)):
    return crud.get_all_subregion(db)


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
        point_start = None
        for key in data_set:
            if str(key).isdigit():
                if not point_start:
                    point_start = float(key)
                else:
                    if float(key) < point_start:
                        point_start = float(key)
            stat_item = {'y': data_set[key]}
            if type_chart == 'column':
                stat_item['name'] = key
            else:
                stat_item['x'] = key
            stat_data.append(stat_item)
        series[0]['data'] = stat_data
        if point_start:
            series[0]['pointStart'] = point_start
        if x_field == 'Var':
            series[0]['pointStart'] = 0
    else:
        series[0]['name'] = 'Error'
#
    return series


def param_value(param: str, item_set: List[schemas.Review]):    # param = Year | Var
    data_set = {}
    for item in item_set:
        data_set[getattr(item, param)] = data_set.get(getattr(item, param), 0) + item.Value
    return data_set


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
