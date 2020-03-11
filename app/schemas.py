from pydantic import BaseModel


class Coordinates(BaseModel):
    lng: int
    lat: int


class EventBase(BaseModel):
    id: int
    name: str
    voivodeship_name: str = None

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    lng: int
    lat: int
    name: str
    description: str
