from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional
from . import models, schemas
import math


def get_organizations_by_building(db: Session, building_id: int):
    return db.query(models.Organization).filter(
        models.Organization.building_id == building_id
    ).options(joinedload(models.Organization.building), joinedload(models.Organization.activities)).all()


def get_organizations_by_activity(db: Session, activity_id: int):
    # Получаем деятельность и все её дочерние деятельности
    activity_ids = get_activity_tree_ids(db, activity_id)

    return db.query(models.Organization).join(
        models.organization_activity
    ).filter(
        models.organization_activity.c.activity_id.in_(activity_ids)
    ).options(joinedload(models.Organization.building), joinedload(models.Organization.activities)).all()


def get_activity_tree_ids(db: Session, activity_id: int) -> List[int]:
    """Получает все ID деятельности в дереве, начиная с указанной"""
    activity_ids = [activity_id]

    def get_children_ids(parent_id: int):
        children = db.query(models.Activity).filter(models.Activity.parent_id == parent_id).all()
        for child in children:
            activity_ids.append(child.id)
            get_children_ids(child.id)

    get_children_ids(activity_id)
    return activity_ids


def get_organizations_in_radius(db: Session, latitude: float, longitude: float, radius_km: float):
    """Поиск организаций в радиусе от точки"""
    # Формула Haversine для расчета расстояния
    organizations = db.query(models.Organization).join(models.Building).options(
        joinedload(models.Organization.building),
        joinedload(models.Organization.activities)
    ).all()

    result = []
    for org in organizations:
        distance = calculate_distance(latitude, longitude, org.building.latitude, org.building.longitude)
        if distance <= radius_km:
            result.append(org)

    return result


def get_organizations_in_rectangle(db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    """Поиск организаций в прямоугольной области"""
    return db.query(models.Organization).join(models.Building).filter(
        and_(
            models.Building.latitude >= min_lat,
            models.Building.latitude <= max_lat,
            models.Building.longitude >= min_lon,
            models.Building.longitude <= max_lon
        )
    ).options(joinedload(models.Organization.building), joinedload(models.Organization.activities)).all()


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Расчет расстояния между двумя точками по формуле Haversine"""
    R = 6371  # Радиус Земли в км

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_all_buildings(db: Session):
    return db.query(models.Building).all()


def get_organization_by_id(db: Session, org_id: int):
    return db.query(models.Organization).filter(
        models.Organization.id == org_id
    ).options(joinedload(models.Organization.building), joinedload(models.Organization.activities)).first()


def search_organizations_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).filter(
        models.Organization.name.ilike(f"%{name}%")
    ).options(joinedload(models.Organization.building), joinedload(models.Organization.activities)).offset(skip).limit(
        limit).all()


def create_building(db: Session, building: schemas.BuildingCreate):
    db_building = models.Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def create_activity(db: Session, activity: schemas.ActivityCreate):
    # Проверяем уровень вложенности
    if activity.parent_id:
        parent = db.query(models.Activity).filter(models.Activity.id == activity.parent_id).first()
        if parent and parent.level >= 3:
            raise ValueError("Максимальный уровень вложенности - 3")
        activity.level = parent.level + 1 if parent else 1

    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def create_organization(db: Session, organization: schemas.OrganizationCreate):
    org_data = organization.dict()
    activity_ids = org_data.pop('activity_ids', [])

    db_organization = models.Organization(**org_data)
    db.add(db_organization)
    db.flush()

    # Добавляем связи с деятельностями
    if activity_ids:
        activities = db.query(models.Activity).filter(models.Activity.id.in_(activity_ids)).all()
        db_organization.activities = activities

    db.commit()
    db.refresh(db_organization)
    return db_organization