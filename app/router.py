from typing import List

from fastapi import APIRouter, HTTPException

from . import schemas, crud

router = APIRouter()


@router.post("/check-voiv/")
async def read_voivodeship(payload: schemas.Coordinates):
    voivodeship = await crud.get_voivodeship_by_point_coordinates(payload.lat, payload.lng)
    if voivodeship is None:
        raise HTTPException(status_code=404, detail="Point outside of Poland")
    return {'voivodeship': voivodeship.get('name')}


@router.get("/events/", response_model=List[schemas.EventBase])
async def read_events(skip: int = 0, limit: int = 10):
    events = await crud.get_events(skip=skip, limit=limit)
    return events


@router.post("/create-event/", response_model=schemas.EventBase, status_code=201)
async def create_event(payload: schemas.EventCreate):
    event = await crud.create_event(payload)
    if event is None:
        raise HTTPException(status_code=400, detail="Event outside of Poland")
    return event


@router.get("/event/{event_id}", response_model=schemas.EventBase)
async def read_event(event_id: int):
    event = await crud.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
