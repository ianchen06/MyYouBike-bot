import math

from config import *


async def fetch_taoyuan_youbike(session):
    return await fetch(session, TAOYUAN_UBIKE_URL)

async def fetch_youbike(session):
    return await fetch(session, UBIKE_URL)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def reply(session, data):
    headers = {
        'Authorization': 'Bearer %s' % ACCESS_TOKEN
    }
    async with session.post(REPLY_URL, json=data, headers=headers) as response:
        return await response.text()


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
