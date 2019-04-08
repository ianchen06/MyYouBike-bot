import aiohttp
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

import utils
from config import *
import handlers

app = Starlette(debug=False)


@app.route('/', methods=['GET', 'POST'])
async def homepage(request):
    print(request.method)
    if request.method == "GET":
        resp = {"status": "ok"}
        return JSONResponse(resp)
    if request.method == "POST":
        body = await request.json()
        reply_token = body.get('events')[0].get('replyToken')
        rcv_msg = body.get('events')[0].get('message')

        if rcv_msg.get('type', '') == 'location':
            resp = await handlers.handle_location(rcv_msg, reply_token)
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

        async with aiohttp.ClientSession() as session:
            r = await utils.reply(session, resp)
            print(r)
        return JSONResponse(resp)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
