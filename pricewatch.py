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

itemListMap = {}
r = emitRequest('https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch.json')
itemList = []

for item in r.json():
    brand = {
        "en": item['brand']['en'],
        "tc": item['brand']['zh-Hant'],
        "sc": item['brand']['zh-Hans']
    }
    
    name = {
        "en": item['name']['en'],
        "tc": item['name']['zh-Hant'],
        "sc": item['name']['zh-Hans']
    }
    
    cat1 = {
        "en": item['cat1Name']['en'],
        "tc": item['cat1Name']['zh-Hant'],
        "sc": item['cat1Name']['zh-Hans']
    }
    
    cat2 = {
        "en": item['cat2Name']['en'],
        "tc": item['cat2Name']['zh-Hant'],
        "sc": item['cat2Name']['zh-Hans']
    }
    
    cat3 = {
        "en": item['cat3Name']['en'],
        "tc": item['cat3Name']['zh-Hant'],
        "sc": item['cat3Name']['zh-Hans']
    }

    supermarketCode = []
    prices = item['prices']
    offers = item['offers']
    prices_map = {}
    offers_map = {}
    
    for item_offer in offers:
        offers_map[item_offer['supermarketCode']] = {
            "supermarketCode": item_offer['supermarketCode'],
            "en": item_offer['en'],
            "tc": item_offer['zh-Hant'],
            "sc": item_offer['zh-Hans']
        }
        #prices_map[item_offer['supermarketCode']]['offer'] = item_offer

    for item_price in prices:
        #item_price['offer'] = offers_map[item_price['supermarketCode']]
        prices_map[item_price['supermarketCode']] = item_price
        supermarketCode.append(item_price['supermarketCode'])
        

    itemList.append({
        "code": item['code'],
        "brand": brand,
        "name": name,
        "cat1": cat1,
        "cat2": cat2,
        "cat3": cat3,
        "prices": prices_map,
        "offers": offers_map,
        "supermarketCode": supermarketCode
    })
    
    itemListMap[item['code']] = {
        "code": item['code'],
        "brand": brand,
        "name": name,
        "cat1": cat1,
        "cat2": cat2,
        "cat3": cat3,
        "prices": prices_map,
        "offers": offers_map,
        "supermarketCode": supermarketCode
    }
}
    
    
    
with open(PRICEWATCH_ITEMLIST, 'w') as f:
  f.write(json.dumps(itemList, ensure_ascii=False))
with open(PRICEWATCH_MAP_ITEMLIST, 'w') as f:
  f.write(json.dumps(itemListMap, ensure_ascii=False))


    
