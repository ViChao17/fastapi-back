from pydantic import BaseModel


class Review(BaseModel):
    id: int
    Country: str
    Year: int
    Region: str
    SubRegion: str
    OPEC: bool
    EU: bool
    OECD: bool
    CIS: bool
    Var: str
    Value: float

    class Config:
        orm_mode = True

