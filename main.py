import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


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


@app.get("/", response_model=Diagram)
async def read_root():
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
