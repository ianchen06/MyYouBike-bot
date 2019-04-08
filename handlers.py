import json
import aiohttp

import templates
import utils


async def handle_location(rcv_msg, reply_token):
    query_lat_lng = (
        float(
            rcv_msg.get('latitude')), float(
            rcv_msg.get('longitude')),)
    async with aiohttp.ClientSession() as session:
        bike_data = await utils.fetch_youbike(session)
        bike_data_list = [v for k, v in json.loads(
            bike_data).get('retVal').items()]
        lat_lng_dict = {(float(v.get('lat')), float(
            v.get('lng'))): v for v in bike_data_list}
        res = []
        for ea in lat_lng_dict:
            res.append((utils.distance(query_lat_lng, ea), lat_lng_dict[ea]))
        top3 = sorted(res, key=lambda x: x[0])[:3]
    msg = []
    render_stn = templates.make_render_stn(query_lat_lng)
    for stn in top3:
        msg.append(render_stn(stn))
    print(msg)
    flx_msg = {
        "type": "carousel",
        "contents": msg
    }
    msg = [
        {"type": "flex",
         "altText": "text",
         "contents": flx_msg}

    ]

    return {
        'replyToken': reply_token,
        'messages': msg
    }
