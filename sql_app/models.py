from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


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
