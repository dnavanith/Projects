import requests
import time
import json
import base64
import hmac
import hashlib
import math

# KuCoin API Credentials
api_key = "x"
api_secret = "x"
api_passphrase = "x"

SYMBOL = "USDTM"  # Trading pair
ORDER_SIDE = "buy"  # 'buy' for long, 'sell' for short
PRICE = 1  # Set your desired entry price
LEVERAGE = 50  # Leverage level

# Calculate order size (Example: Using 1 USDT for position)
SIZE = 1  # Ensure integer size

def place_order():
    url = "https://api-futures.kucoin.com/api/v1/orders"
    order_data = {
        "clientOid": str(int(time.time() * 1000)),
        "side": ORDER_SIDE,
        "symbol": SYMBOL,
        "type": "market",
        "price": str(PRICE),
        "size": str(SIZE),
        "leverage": 30,
        "marginMode": "ISOLATED",
        "timeInForce": "GTC",
    }

    timestamp = str(int(time.time() * 1000))
    data_json = json.dumps(order_data)
    prehash_string = timestamp + 'POST' + '/api/v1/orders' + data_json
    signature = base64.b64encode(hmac.new(api_secret.encode(), prehash_string.encode(), hashlib.sha256).digest()).decode()
    passphrase = base64.b64encode(hmac.new(api_secret.encode(), api_passphrase.encode(), hashlib.sha256).digest()).decode()

    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": timestamp,
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=data_json)
    if response.status_code == 200:
        print("✅ Order placed successfully!", response.json())
        order_id = response.json().get("data", {}).get("orderId", "")
    else:
        print("❌ Failed to place order:", response.json())


place_order()
SIZE = 2

urlprice = f"https://api-futures.kucoin.com/api/v1/mark-price/{SYMBOL}/current"
prevPrice=0.1539
totalProfit=0
final=0
while True:
    try:
        response = requests.get(urlprice)
        data = response.json()
        
        if "data" in data:
            mark_price = data["data"]["value"]
            print(f"Mark Price: {mark_price}")
        else:
            print("Error: Unexpected response format", data)

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        
    # Fetch price every second
    pd=((mark_price - prevPrice) / prevPrice) * 100
    
    prevPrice=mark_price
    if pd>0:
        if ORDER_SIDE!="buy":
            ORDER_SIDE = "buy"
            place_order()
            
    elif pd<0:
        if ORDER_SIDE!="sell":
            ORDER_SIDE = "sell"
            place_order()

    time.sleep(1)




