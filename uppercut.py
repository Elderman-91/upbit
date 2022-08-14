import datetime
import time
import jwt
import hashlib
import requests
import uuid
from urllib.parse import urlencode, unquote
from sys import exit

min_won = 5001
time_over = False
local_time = datetime.datetime.now()
def place_order(ask_price):
    access_key = 'key'
    secret_key = 'key'
    server_url = 'https://api.upbit.com'

    params = {
        'market': 'KRW-BTT',
        'side': 'bid',
        'ord_type': 'limit',
        'price': str(ask_price),
        'volume': str(round(min_won/ask_price, 8))
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
      'Authorization': authorization,
    }
    time1 = datetime.datetime.now()
    print("time1 =" + str(time1))
    res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
    time2 = datetime.datetime.now()
    print("time2 =" + str(time2))
    
    print(time2 - time1)
    res.json()
    print(res.json()["created_at"])

try:
    while True:
        ref_time = datetime.datetime.now()
        hr = ref_time.hour
        min = ref_time.minute
        second = ref_time.second
        ms = ref_time.microsecond
        print("C upbit time is: " + str(ref_time))

        if hr == 8 and min == 59 and second == 59 and ms >= 650000:
            url1 = "https://api.upbit.com/v1/trades/ticks?market=KRW-BTT&count=1"
            headers1 = {"Accept": "application/json"}
            response1 = requests.get(url1, headers=headers1)
            data1 = response1.json()
            last_price = data1[0]["trade_price"]

            url2 = "https://api.upbit.com/v1/orderbook?markets=KRW-BTT&orderbook_unit=15"

            headers2 = {"Accept": "application/json"}

            response2 = requests.get(url2, headers=headers2)
            data2 = response2.json()
            ask_price =data2[0]["orderbook_units"][0]["ask_price"]
            if last_price == ask_price:
                print("UP")
            else:
                print("DOWN")
                place_order(ask_price)
        if hr == 9 and min > 0:
            time_over = True
        time.sleep(0.07)

except KeyboardInterrupt or time_over is True:
    print("STOP")
    exit()
