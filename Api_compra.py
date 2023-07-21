import time
import requests
import hmac
from hashlib import sha256
import json

APIURL = "https://open-api.bingx.com"
API_KEY = "H6q86uSwZPvnYT0KYdBe4ARqPsvRx2NX40z3IbwWXRBQlYJXiaurHneRg5XGuIZRNTxjo2csu5obknLRXA"
SECRET_KEY = "zxiKY5cDIiLhf5kZprGSJXycMpHBKoT2OitLfCITAq3HKOx3U2RB57dJlTK6Yosi2XM2mtEv2KcOcqw8kd4Exw"

# Funciones de consulta y manejo de respuesta JSON

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    return signature

def send_request(method, path, urlpa, payload):
    url = f"{APIURL}{path}?{urlpa}&signature={get_sign(SECRET_KEY, urlpa)}"
    headers = {
        'X-BX-APIKEY': API_KEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text

def get_server_time():
    path = '/openApi/swap/v2/server/time'
    url = APIURL + path
    response = requests.get(url)
    if response.status_code == 200:
        server_time = response.json()['data']['serverTime']
        return server_time
    else:
        print("Error al obtener la hora del servidor")
        return None

def praseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join([f"{x}={paramsMap[x]}" for x in sortedKeys])
    return paramsStr + f"&timestamp={int(time.time() * 1000)}"

# Consulta de BTC-USDT
def consulta():
    payload = {}
    path = '/openApi/swap/v2/quote/price'
    method = "GET"
    paramsMap = {
        "symbol": "BTC-USDT"
    }
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

# Consulta de mi balance
def balance_cuenta():
    payload = {}
    path = '/openApi/swap/v2/user/balance'
    method = "GET"
    paramsMap = {
        "timestamp": int(get_server_time()),
        "recvWindow": 0
    }
    paramsStr = praseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

# Funciones principales

if __name__ == '__main__':
    response_text = consulta()
    response_data = json.loads(response_text)
    symbol = response_data['data']['symbol']
    price = response_data['data']['price']

    try:
        price_float = float(price)
        print("Symbol:", symbol)
        print("Price (float):", price_float)
    except ValueError:
        print("Error: El valor de 'price' no es un número válido")

    response_text = balance_cuenta()
    response_data = json.loads(response_text)
    balance_data = response_data['data']['balance']
    asset = balance_data['asset']
    balance = balance_data['balance']
    balance_entero = int(float(balance))
    print("Asset:", asset)
    print("Balance (entero):", balance_entero)

    # Preparando compra
    compra = (balance_entero-2) / price_float
    compra_truncada = "{:.4f}".format(compra)
    print("LA COMPRA SERÍA DE: ", compra_truncada)

    # Orden de comprar BTC-USDT
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    timestamp = int(time.time() * 1000)  # Tiempo actual en milisegundos
    paramsMap = {
        "symbol": "BTC-USDT",
        "type": "MARKET",
        "side": "BUY",
        "positionSide": "LONG",
        "price": .0,
        "quantity": compra_truncada,
        "stopPrice": .0,
        "timestamp": timestamp,  # Usar el tiempo actual
        "recvWindow": 0,
        "timeInForce": ""
    }
    paramsStr = praseParam(paramsMap)
    response_text = send_request(method, path, paramsStr, payload)
    print("demo:", response_text)
