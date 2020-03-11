import asyncio
import json

from colorama import Fore
from geoalchemy2 import WKTElement

from app import models, database


def prepare_for_wktelement(coordinates):
    coordinates = str(coordinates).replace(',', '').replace('[', '').replace(']', ',')[:-2]
    polygon = WKTElement(f"Polygon (({coordinates}))", srid=4326)
    return polygon


with open('voivodeships_data.json') as file:
    voivodeships_data = json.load(file).get('data')


async def save_data_to_db(data: dict):
    await database.database.connect()
    for d in data:
        name = d.get('name').title()
        query = models.voivodeships.select().where(models.voivodeships.c.name == name)
        voivodeship = await database.database.fetch_one(query=query)
        if voivodeship:
            print(Fore.RED + f"{name} is already in DB", flush=True)
            continue
        polygon = prepare_for_wktelement(d.get('area'))
        query = models.voivodeships.insert().values(
            name=name.title(),
            area=polygon
        )
        await database.database.execute(query=query)
        print(Fore.YELLOW + f"{name} saved", flush=True)
    await database.database.disconnect()

asyncio.run(save_data_to_db(voivodeships_data))
