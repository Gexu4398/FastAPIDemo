from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 添加根路径重定向
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

# 获取所有城市
@app.get("/cities/", response_model=List[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    cities = db.query(models.City).offset(skip).limit(limit).all()
    return cities

# 根据ID获取特定城市
@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(database.get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

# 创建新城市
@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    db_city = models.City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

# 更新城市
@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(database.get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    
    db_city.name = city.name
    db.commit()
    db.refresh(db_city)
    return db_city

# 删除城市
@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(database.get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    
    db.delete(db_city)
    db.commit()
    return {"message": "City deleted successfully"} 