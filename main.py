import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from add_review_from_csv import set_review
from threading import Thread
from typing import Optional


data = {
    'xLabel': 'X',
    'yLabel': 'Y',
    'data': {
        'A': 5,
        'B': 10,
        'C': 15
    }
}


class Diagram(BaseModel):
    xLabel: str
    yLabel: str
    data: dict


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


@app.get("/", response_model=Diagram)
async def read_root():
    return data


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/review/", response_model=List[schemas.Review])
def get_review(skip: int = 0, limit: int = 100, var: Optional[str] = None, db: Session = Depends(get_db)):
    if var:
        items = crud.get_review_by_var(db, skip=skip, limit=limit, var=var)
    else:
        items = crud.get_review(db, skip=skip, limit=limit)
    return items


@app.get("/review/{var}", response_model=List[schemas.Review])
def get_review_by_var(skip: int = 0, limit: int = 100, var: str = '', db: Session = Depends(get_db)):
    items = crud.get_review_by_var(db, skip=skip, limit=limit, var=var)
    return items


@app.get("/test/")
def get_test(db: Session = Depends(get_db)):
    return crud.get_full_review_by_country(db=db, country=[])

# @app.get("/review/")
# def add_review(db: Session = Depends(get_db)):
#     thread = Thread(target=set_review, args=(db, ))
#     thread.start()
#     thread.join()
#     return {'status': 'OK'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
