from pprint import pprint
import gzip
import json
import math
import asyncio
import os
import math

import aiohttp
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

app = Starlette(debug=False)

REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
UBIKE_URL = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'

ACCESS_TOKEN = os.getenv("CHANNEL_TOKEN")

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

async def fetch_youbike(session):
    return await fetch(session, UBIKE_URL)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def reply(session, data):
    headers = {
            'Authorization': 'Bearer %s'%ACCESS_TOKEN
            }
    async with session.post(REPLY_URL, json=data, headers=headers) as response:
        return await response.text()

@app.route('/', methods=['GET','POST'])
async def homepage(request):
    body = await request.json()
    # pprint(body)
    rcv_msg = body.get('events')[0].get('message')
    if rcv_msg.get('type') == 'location':
        # print('doing location')
        query_lat_lng = (float(rcv_msg.get('latitude')), float(rcv_msg.get('longitude')),)
        async with aiohttp.ClientSession() as session:
            bike_data = await fetch_youbike(session)
            bike_data_list = [v for k,v in json.loads(bike_data).get('retVal').items()]
            lat_lng_dict = {(float(v.get('lat')), float(v.get('lng'))): v for v in bike_data_list}
            res = []
            for ea in lat_lng_dict:
                # print("Comparing ")
                res.append((distance(query_lat_lng, ea), lat_lng_dict[ea]))
            top3 = sorted(res, key=lambda x: x[0])[:3]
            # pprint(top3)
        msg = [{'type': "location", "title": stn[1].get('sna'), "address": stn[1].get('ar'), "latitude": stn[1].get('lat'), "longitude": stn[1].get('lng')} for stn in top3]
        # pprint(msg)

        resp = {
                'replyToken': body.get('events')[0].get('replyToken'),
                'messages': msg
                }
    else:
        qr = {
                "type": "text",
                "text": "請傳送位置訊息給我",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type": "location",
                                "label": "傳送位置訊息"
                                }
                            }
                        ]
                    }
                }
        resp = {
                'replyToken': body.get('events')[0].get('replyToken'),
                'messages': [qr]
                }

        # TODO: display direction to ubike station
        # https://www.google.com/maps/dir/?api=1&origin=Space+Needle+Seattle+WA&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling
        async with aiohttp.ClientSession() as session:
            bike_data = await fetch_youbike(session)
        bike_data_list = [v for k,v in json.loads(bike_data).get('retVal').items()]
        # pprint({(v.get('lat'), v.get('lng')): v for v in bike_data_list})
    async with aiohttp.ClientSession() as session:
        r = await reply(session, resp)
        print(r)
    return JSONResponse(resp)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
