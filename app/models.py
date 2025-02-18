from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.schema import Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, Sequence('city_seq'), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    country = Column(String(100))
    province = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # 关系
    districts = relationship("District", back_populates="city", cascade="all, delete-orphan")
    population_stats = relationship("PopulationStats", back_populates="city", cascade="all, delete-orphan")

class District(Base):
    __tablename__ = "district"

    id = Column(BigInteger, Sequence('district_seq'), primary_key=True, index=True)
    city_id = Column(BigInteger, ForeignKey('city.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    area_size = Column(DECIMAL(10,2))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # 关系
    city = relationship("City", back_populates="districts")

class PopulationStats(Base):
    __tablename__ = "population_stats"

    id = Column(BigInteger, Sequence('population_seq'), primary_key=True, index=True)
    city_id = Column(BigInteger, ForeignKey('city.id', ondelete='CASCADE'))
    year = Column(Integer, nullable=False)
    total_population = Column(Integer, nullable=False)
    urban_population = Column(Integer)
    rural_population = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # 关系
    city = relationship("City", back_populates="population_stats") 