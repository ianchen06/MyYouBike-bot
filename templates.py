from config import *


def make_render_stn(query_lat_lng):
    def render_stn(stn):
        return {
            "type": "bubble",
            "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": "https://api.mapbox.com/v4/mapbox.emerald/pin-s-heart+285A98({lng},{lat})/{lng},{lat},17/300x300@2x.png?access_token={access_token}".format(lng=stn[1].get('lng'), lat=stn[1].get('lat'), access_token=MAPBOX_ACCESS_TOKEN)
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                        {
                            "type": "text",
                            "text": "{title}".format(title=stn[1].get('sna')),
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl"
                        },
                    {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "{no_rentable} 可借/{no_returnable} 可還".format(no_rentable=int(stn[1].get('sbi')), no_returnable=int(stn[1].get('tot')) - int(stn[1].get('sbi'))),
                                    "wrap": True,
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0
                                }
                            ]
                        }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "用Google Map開啟",
                                "uri": "https://www.google.com/maps/search/?api=1&query={lat},{lng}".format(lng=stn[1].get('lng'), lat=stn[1].get('lat'))
                            }
                        },
                    {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "帶我去",
                                "uri": "https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&travelmode=walking".format(
                                    origin_lat=query_lat_lng[0],
                                    origin_lng=query_lat_lng[1],
                                    dest_lat=stn[1].get('lat'),
                                    dest_lng=stn[1].get('lng')
                                )
                            }
                        }
                ]
            }
        }

    return render_stn
