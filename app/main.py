from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import time

from . import models, schemas, database
from .config import get_settings
from .logger import setup_logger
from .middleware import error_handler_middleware

settings = get_settings()
logger = setup_logger(__name__)

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 添加中间件
app.middleware("http")(error_handler_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# API性能监控中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request processed in {process_time:.4f} seconds")
    return response

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# 城市相关的API端点
@app.get("/cities/", response_model=List[schemas.City])
def read_cities(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    logger.info(f"Fetching cities with skip={skip}, limit={limit}")
    cities = db.query(models.City).offset(skip).limit(limit).all()
    return cities

@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Fetching city with id={city_id}")
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        logger.warning(f"City with id={city_id} not found")
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    logger.info(f"Creating new city with name={city.name}")
    db_city = models.City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, 
    city: schemas.CityCreate, 
    db: Session = Depends(database.get_db)
):
    logger.info(f"Updating city with id={city_id}")
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        logger.warning(f"City with id={city_id} not found")
        raise HTTPException(status_code=404, detail="City not found")
    
    db_city.name = city.name
    db.commit()
    db.refresh(db_city)
    return db_city

@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Deleting city with id={city_id}")
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        logger.warning(f"City with id={city_id} not found")
        raise HTTPException(status_code=404, detail="City not found")
    
    db.delete(db_city)
    db.commit()
    return {"message": "City deleted successfully"} 