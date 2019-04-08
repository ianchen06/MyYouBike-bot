from config import *


def render_google_maps(args):
    return """<!doctype html>
<html>
<head>
    <script>
    window.onload = function() {{
      console.log(navigator.userAgent)
      console.log(navigator.userAgent.indexOf('iPhone'))
      if(navigator.userAgent.indexOf('iPhone') > -1){{
        window.location = "comgooglemapsurl://www.google.com/maps/search/?api=1&query={lat},{lng}"
      }} else if(navigator.userAgent.indexOf('Android') > -1){{
        window.location = "https://www.google.com/maps/search/?api=1&query={lat},{lng}"
      }} else {{
        window.location = "https://www.google.com/maps/search/?api=1&query={lat},{lng}"
      }}
      setTimeout(x=>window.location="https://www.google.com/maps/search/?api=1&query={lat},{lng}", 2000)
    }}
    </script>
</head>
<body>
</body>
</html>""".format(lng=args.query_params['lng'], lat=args.query_params['lat'])


def make_render_stn(query_lat_lng):
    def render_stn(stn):
        return {
            "type": "bubble",
            "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": "https://api.mapbox.com/v4/mapbox.emerald/pin-s-heart+285A98({lng},{lat})/{lng},{lat},17/300x300@2x.png?access_token={access_token}".format(lng=stn[1].get('lng').strip(), lat=stn[1].get('lat').strip(), access_token=MAPBOX_ACCESS_TOKEN),
                    "action": {
                        "type": "uri",
                        "label": "用Google Maps開啟",
                        "uri": "https://{app_url}/maps?lat={lat}&lng={lng}".format(app_url=APP_URL, lng=stn[1].get('lng').strip(), lat=stn[1].get('lat').strip())
                    }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                        {
                            "type": "text",
                            "text": "{title}[{dist}m]".format(title=stn[1].get('sna'), dist=int(stn[0] * 1000)),
                            "wrap": True,
                            # "weight": "bold",
                            "size": "lg",
                            "color": "#929292"
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
                                "label": "用Google Maps開啟",
                                # "uri": "https://www.google.com/maps/search/?api=1&query={lat},{lng}".format(lng=stn[1].get('lng').strip(), lat=stn[1].get('lat').strip())
                                "uri": "https://{app_url}/maps?lat={lat}&lng={lng}".format(app_url=APP_URL, lng=stn[1].get('lng').strip(), lat=stn[1].get('lat').strip())
                            }
                        }  # ,
                    # {
                    #         "type": "button",
                    #         "action": {
                    #             "type": "uri",
                    #             "label": "帶我去",
                    #             "uri": "https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&travelmode=walking".format(
                    #                 origin_lat=query_lat_lng[0],
                    #                 origin_lng=query_lat_lng[1],
                    #                 dest_lat=stn[1].get('lat').strip(),
                    #                 dest_lng=stn[1].get('lng').strip()
                    #             )
                    #         }
                    #     }
                ]
            }
        }

    return render_stn
