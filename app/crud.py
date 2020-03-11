from geoalchemy2 import WKTElement

from . import models, database, schemas


async def get_voivodeship(lat: int, lng: int):
    point = WKTElement(f'POINT({lat} {lng})', srid=4326)
    query = models.voivodeships.select().where(
        models.voivodeships.c.area.ST_contains(point)
    )
    voivodeship = await database.database.fetch_one(query=query)
    if voivodeship is None:
        return None
    voivodeship = dict(voivodeship)
    return voivodeship


async def get_voivodeship_by_id(v_id: int):
    query = models.voivodeships.select().where(models.voivodeships.c.id == v_id)
    voivodeship = await database.database.fetch_one(query=query)
    if voivodeship is None:
        return None
    voivodeship = dict(voivodeship)
    return voivodeship


async def get_events(skip: int, limit: int):
    query = models.events.select().limit(limit).offset(skip)
    events = await database.database.fetch_all(query=query)
    events = [dict(event) for event in events]
    for event in events:
        voivodeship = await get_voivodeship_by_id(event.get('voivodeship_id'))
        event['voivodeship_name'] = voivodeship.get('name')
    return [dict(event) for event in events]


async def get_event(event_id: int):
    query = models.events.select().where(
        models.events.c.id == event_id
    )
    event = await database.database.fetch_one(query=query)
    if event is None:
        return None
    event = dict(event)
    voivodeship = await get_voivodeship_by_id(event.get('voivodeship_id'))
    event['voivodeship_name'] = voivodeship.get('name')
    return dict(event)


async def create_event(event: schemas.EventCreate):
    voivodeship = await get_voivodeship(lat=event.lat, lng=event.lng)
    query = models.events.insert().values(
        name=event.name,
        description=event.description,
        voivodeship_id=voivodeship.get('id')
    )
    event = await database.database.execute(query=query)
    event = await get_event(event_id=event)
    return event
