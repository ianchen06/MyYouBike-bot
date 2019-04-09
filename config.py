import os

REPLY_URL = 'https://api.line.me/v2/bot/message/reply'
UBIKE_URL = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.gz'
TAOYUAN_UBIKE_URL = 'https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c&rid=a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f'
NEWTPE_UBIKE_URL = 'http://data.ntpc.gov.tw/api/v1/rest/datastore/382000000A-000352-001'
TAINAN_TBIKE_URL = 'http://tbike.tainan.gov.tw:8081/Service/StationStatus/Json'
HSHINCHU_YOUBIKE_URL = 'http://opendata.hccg.gov.tw/dataset/1f334249-9b55-4c42-aec1-5a8a8b5e07ca/resource/4d5edb22-a15e-4097-8635-8e32f7db601a/download/20180702150422381.json'

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
ACCESS_TOKEN = os.getenv("CHANNEL_TOKEN")

APP_URL = os.getenv("APP_URL") or '7162af34.ngrok.io'
