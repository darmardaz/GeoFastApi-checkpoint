from typing import List
from fastapi import APIRouter, HTTPException
from . import schemas, crud

router = APIRouter()


@router.post("/check-voiv/")
async def read_voivodeships(payload: schemas.Coordinates):
    voivodeship = await crud.get_voivodeship(payload.lat, payload.lng)
    if voivodeship is None:
        raise HTTPException(status_code=404, detail="Point outside of Poland")
    return {'voivodeship': voivodeship.get('name')}


@router.get("/events/", response_model=List[schemas.EventBase])
async def read_events(skip: int = 0, limit: int = 10):
    events = await crud.get_events(skip=skip, limit=limit)
    return events


@router.post("/create-event/", response_model=schemas.EventBase)
async def create_events(payload: schemas.EventCreate):
    event = await crud.create_event(payload)
    return event


@router.post("/event/{event_id}", response_model=schemas.EventBase)
async def create_events(event_id: int):
    event = await crud.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="User not found")
    return event
