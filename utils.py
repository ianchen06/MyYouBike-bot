import json
import math

from config import *


async def fetch_and_parse_taoyuan(session):
    resp = await fetch(session, TAOYUAN_UBIKE_URL)
    return [v for k, v in json.loads(resp).get('retVal').items()]

async def fetch_and_parse_tpe(session):
    resp = await fetch(session, UBIKE_URL)
    return [v for k, v in json.loads(resp).get('retVal').items()]

async def fetch_and_parse_newtpe(session):
    resp = await fetch(session, NEWTPE_UBIKE_URL)
    return json.loads(resp).get('result').get('records')


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
