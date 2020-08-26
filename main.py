import requests
import time

ids = []
cookie = open('cookie.txt','r').readline().strip()

def getIds(cursor):
  if cursor == None:
      r = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&cursor=1_2_38d43aaad573938654a22a6ae8524251&limit=60&maxPrice=0&minPrice=0').json()
  else:
      r = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&cursor={cursor}&limit=60&maxPrice=0&minPrice=0').json()
  for noob in r['data']:
      id = noob['id']
      if noob['itemType'] == 'Asset':
          p = requests.get(f'https://api.roblox.com/Marketplace/ProductInfo?assetId={id}').json()
          ids.append(p['ProductId'])
      else:
          p = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
          ids.append(p['product']['id'])
  ncursor = r['nextPageCursor']
  if ncursor != None: getIds(ncursor)
  else: print('Finished Scraping AssetIDs!')

req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie
try:
  r = req.get('http://www.roblox.com/mobileapi/userinfo').json()
  r = req.post('https://www.roblox.com/api/item.ashx?')
  xcrsftoken = r.headers['X-CSRF-TOKEN']
except:
  input('invalid cookie change in cookie.txt')
  exit()

print('scraping itemids')
getIds(None)

print('buying items')
for id in ids:
  r = req.post(f'https://economy.roblox.com/v1/purchases/products/{id}', data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1} ,headers={"X-CSRF-TOKEN": xcrsftoken})
  if 'TooManyRequests' in r.text:
      print('Too many requests, waiting 60 sec')
      ids.append(id)
      time.sleep(60)