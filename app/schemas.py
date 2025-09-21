from pydantic import BaseModel, Field
from typing import List, Optional

class BuildingBase(BaseModel):
    address: str
    latitude: float = Field(..., ge=-90, le=90, description="Широта от -90 до 90")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота от -180 до 180")

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    level: int = Field(default=1, ge=1, le=3, description="Уровень вложенности (1-3)")

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    children: List['Activity'] = []

    class Config:
        from_attributes = True

Activity.model_rebuild()

class OrganizationBase(BaseModel):
    name: str
    phone_numbers: List[str]
    building_id: int

class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []

class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity] = []

    class Config:
        from_attributes = True

class OrganizationSearch(BaseModel):
    organizations: List[Organization]
    total: int
