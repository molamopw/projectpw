import requests
import json
from os import path
import copy
import os
import time

def emitRequest(url):
  # retry if "Too many request (429)"
  while True:
    r = requests.get(url)
    if r.status_code == 200:
      return r
    elif r.status_code == 429:
      time.sleep(1)
    else:
      raise Exception(r.status_code, url)


# define output name
PRICEWATCH_ITEMLIST = 'pricewatch_itemlist.json'
PRICEWATCH_MAP_ITEMLIST = 'pricewatch_map_itemlist.json'

if path.isfile(PRICEWATCH_ITEMLIST):
  os.remove(PRICEWATCH_ITEMLIST)
if path.isfile(PRICEWATCH_MAP_ITEMLIST):
  os.remove(PRICEWATCH_MAP_ITEMLIST)

itemList = {}
r = emitRequest('https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch.json')
itemList = []

for item in r.json():
    brandList = []
    brandList.append({
        "en": item['brand']['en'],
        "tc": item['brand']['zh-Hant'],
        "sc": item['brand']['zh-Hans']
    })

    itemList.append({
        "code": item['code'],
        "brand": brandList
    })
    
with open(PRICEWATCH_ITEMLIST, 'w') as f:
  f.write(json.dumps(itemList, ensure_ascii=False))
    
    
