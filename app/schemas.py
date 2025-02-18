from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

# District schemas
class DistrictBase(BaseModel):
    name: str = Field(max_length=100)
    area_size: Optional[Decimal] = None

class DistrictCreate(DistrictBase):
    pass

class District(DistrictBase):
    id: int
    city_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Population stats schemas
class PopulationStatsBase(BaseModel):
    year: int
    total_population: int
    urban_population: Optional[int] = None
    rural_population: Optional[int] = None

class PopulationStatsCreate(PopulationStatsBase):
    pass

class PopulationStats(PopulationStatsBase):
    id: int
    city_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# City schemas
class CityBase(BaseModel):
    name: str = Field(max_length=100)
    country: Optional[str] = None
    province: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class City(CityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    districts: List[District] = []
    population_stats: List[PopulationStats] = []

    class Config:
        from_attributes = True

# 统计数据响应模型
class CityStats(BaseModel):
    total_cities: int
    total_districts: int
    total_population: int
    avg_district_per_city: float
    latest_update: datetime 