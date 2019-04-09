import os

REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
UBIKE_URL = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'
TAOYUAN_UBIKE_URL = 'https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c&rid=a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f'

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
ACCESS_TOKEN = os.getenv("CHANNEL_TOKEN")

APP_URL = os.getenv("APP_URL") or '7162af34.ngrok.io'
