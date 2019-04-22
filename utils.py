import json
import math
import time

from config import *

# TODO: BORKEN.....
async def fetch_and_parse_hsinchu(session):
    # t1 = time.time()
    resp = await fetch(session, HSHINCHU_YOUBIKE_URL)
    # print("[fetch_and_parse_taoyuan] start: %s, used: %s"%(t1, time.time() - t1))
    print(resp)
    data = []
    for r in json.loads(resp):
        d = {"sbi": r.get('車柱數'),
             "sna": r.get('站點名稱'),
             "tot": r.get('車柱數'),
             "lat": str(r.get('緯度')),
             "lng": str(r.get('經度'))}
        data.append(d)

    return data

async def fetch_and_parse_tainan(session):
    # t1 = time.time()
    resp = await fetch(session, TAINAN_TBIKE_URL)
    # print("[fetch_and_parse_taoyuan] start: %s, used: %s"%(t1, time.time() - t1))
    data = []
    for r in json.loads(resp):
        d = {"sbi": r.get('AvaliableBikeCount'),
             "sna": r.get('StationName'),
             "tot": r.get('Capacity'),
             "lat": str(r.get('Latitude')),
             "lng": str(r.get('Longitude'))}
        data.append(d)

    return data

async def fetch_and_parse_taoyuan(session):
    # t1 = time.time()
    resp = await fetch(session, TAOYUAN_UBIKE_URL)
    # print("[fetch_and_parse_taoyuan] start: %s, used: %s"%(t1, time.time() - t1))
    return [v for k, v in json.loads(resp).get('retVal').items()]

async def fetch_and_parse_tpe(session):
    # t1 = time.time()
    resp = await fetch(session, UBIKE_URL)
    # print("[fetch_and_parse_tpe] start: %s, %s"%(t1, time.time() - t1))
    return [v for k, v in json.loads(resp).get('retVal').items()]

async def fetch_and_parse_newtpe(session):
    # t1 = time.time()
    resp = await fetch(session, NEWTPE_UBIKE_URL)
    # print("[fetch_and_parse_newtpe] start: %s, %s"%(t1, time.time() - t1))
    return json.loads(resp).get('result').get('records')


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text(encoding='utf-8')
    except Exception as e:
        print("[ERROR][%s]%s"%(url, e))
        return []


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
