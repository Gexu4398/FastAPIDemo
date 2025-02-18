from sqlalchemy import Column, BigInteger, String
from sqlalchemy.schema import Sequence
from .database import Base

class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, Sequence('city_seq'), primary_key=True, index=True)
    name = Column(String, index=True) 