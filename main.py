import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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


app = FastAPI()


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
