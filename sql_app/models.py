from sqlalchemy import Boolean, Column, Integer, String, Float

from .database import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    Country = Column(String, index=True)
    Year = Column(Integer, index=True)
    Region = Column(String, index=True)
    SubRegion = Column(String, index=True)
    OPEC = Column(Boolean, default=False)
    EU = Column(Boolean, default=False)
    OECD = Column(Boolean, default=False)
    CIS = Column(Boolean, default=False)
    Var = Column(String, index=True)
    Value = Column(Float)
