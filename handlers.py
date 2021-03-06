import asyncio
import aiohttp

import templates
import utils


async def handle_location(rcv_msg, reply_token):
    query_lat_lng = (
        float(
            rcv_msg.get('latitude')), float(
            rcv_msg.get('longitude')),)
    async with aiohttp.ClientSession() as session:
        wg = await asyncio.gather(*[utils.fetch_and_parse_tpe(session),
                                    utils.fetch_and_parse_newtpe(session),
                                    utils.fetch_and_parse_tainan(session),
                                    # utils.fetch_and_parse_hsinchu(session),
                                    utils.fetch_and_parse_taoyuan(session)])
    # TODO: This assumes TPE and Taoyuan ubike data schema is the same
    # Hsinchu is different....
    # schema
    # {"sbi": <rentable: int>,
    #  "sna": <station_name: str>,
    #  "tot": <total_slots: int>,
    #  "lat": <lat: str>,
    #  "lng": <lng: str>,
    # }
    bike_data_list = []
    for d in wg:
        bike_data_list.extend(d)

    # All bike data in dict {(lat,lng): <youbike_data:dict>}
    lat_lng_dict = {(float(v.get('lat')), float(v.get('lng'))): v for v in bike_data_list}

    # calculate distance between user and every bike stn
    # [(<distance: int>, <youbike_data:dict>)...]
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
