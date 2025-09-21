from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import engine
from .dependencies import get_db
from .auth import verify_api_key

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Orgpipanizations API",
    description="REST API для справочника организаций, зданий и деятельности",
    version="1.0.0"
)

# Все эндпоинты требуют API ключ
@app.get("/organizations/by-building/{building_id}", response_model=List[schemas.Organization])
async def get_organizations_by_building(
    building_id: int,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить все организации в конкретном здании"""
    organizations = crud.get_organizations_by_building(db, building_id)
    return organizations

@app.get("/organizations/by-activity/{activity_id}", response_model=List[schemas.Organization])
async def get_organizations_by_activity(
    activity_id: int,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить все организации по виду деятельности (включая дочерние виды)"""
    organizations = crud.get_organizations_by_activity(db, activity_id)
    return organizations

@app.get("/organizations/in-radius", response_model=List[schemas.Organization])
async def get_organizations_in_radius(
    latitude: float = Query(..., description="Широта центральной точки"),
    longitude: float = Query(..., description="Долгота центральной точки"),
    radius: float = Query(..., description="Радиус поиска в километрах"),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить организации в заданном радиусе от точки"""
    organizations = crud.get_organizations_in_radius(db, latitude, longitude, radius)
    return organizations

@app.get("/organizations/in-rectangle", response_model=List[schemas.Organization])
async def get_organizations_in_rectangle(
    min_lat: float = Query(..., description="Минимальная широта"),
    max_lat: float = Query(..., description="Максимальная широта"),
    min_lon: float = Query(..., description="Минимальная долгота"),
    max_lon: float = Query(..., description="Максимальная долгота"),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить организации в прямоугольной области"""
    organizations = crud.get_organizations_in_rectangle(db, min_lat, max_lat, min_lon, max_lon)
    return organizations

@app.get("/buildings", response_model=List[schemas.Building])
async def get_buildings(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить список всех зданий"""
    buildings = crud.get_all_buildings(db)
    return buildings

@app.get("/organizations/{organization_id}", response_model=schemas.Organization)
async def get_organization(
    organization_id: int,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Получить информацию об организации по ID"""
    organization = crud.get_organization_by_id(db, organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@app.get("/organizations/search/by-name", response_model=List[schemas.Organization])
async def search_organizations_by_name(
    name: str = Query(..., description="Название организации для поиска"),
    skip: int = Query(0, description="Количество пропускаемых записей"),
    limit: int = Query(100, description="Максимальное количество результатов"),
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Поиск организаций по названию"""
    organizations = crud.search_organizations_by_name(db, name, skip, limit)
    return organizations

# Endpoints для создания данных (для тестирования)
@app.post("/buildings", response_model=schemas.Building)
async def create_building(
    building: schemas.BuildingCreate,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Создать новое здание"""
    return crud.create_building(db, building)

@app.post("/activities", response_model=schemas.Activity)
async def create_activity(
    activity: schemas.ActivityCreate,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Создать новый вид деятельности"""
    try:
        return crud.create_activity(db, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/organizations", response_model=schemas.Organization)
async def create_organization(
    organization: schemas.OrganizationCreate,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Создать новую организацию"""
    return crud.create_organization(db, organization)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)