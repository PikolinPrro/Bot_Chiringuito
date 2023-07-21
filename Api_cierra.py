import requests
import hmac
from hashlib import sha256
import json

APIURL = "https://open-api.bingx.com"
API_KEY = "H6q86uSwZPvnYT0KYdBe4ARqPsvRx2NX40z3IbwWXRBQlYJXiaurHneRg5XGuIZRNTxjo2csu5obknLRXA"  # Coloca tu API Key aquí
SECRET_KEY = "zxiKY5cDIiLhf5kZprGSJXycMpHBKoT2OitLfCITAq3HKOx3U2RB57dJlTK6Yosi2XM2mtEv2KcOcqw8kd4Exw"  # Coloca tu Secret Key aqui

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
    server_time = get_server_time()
    return paramsStr + f"&timestamp={server_time}"

# Consulta de posiciones
def consulta_posiciones():
    payload = {}
    path = '/openApi/swap/v2/user/positions'
    method = "GET"
    paramsMap = {
        "symbol": "BTC-USDT",
        "timestamp": int(get_server_time()),
        "recvWindow": 0
    }
    paramsStr = praseParam(paramsMap)
    response_text = send_request(method, path, paramsStr, payload)
    response_data = json.loads(response_text)
    position_data = response_data.get("data")
    if position_data:
        position_amt = position_data[0].get("positionAmt")
        return position_amt
    else:
        print("Error al obtener las posiciones")
        return None

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

if __name__ == '__main__':
    position_amt = consulta_posiciones()
    if position_amt is not None:
        print("Position Amount:", position_amt)

        # Preparando venta
        venta = float(position_amt)
        venta_truncada = "{:.4f}".format(venta)
        print("La venta sería de:", venta_truncada)

        # Orden de vender BTC-USDT
        payload = {}
        path = '/openApi/swap/v2/trade/order'
        method = "POST"
        timestamp = int(get_server_time())
        paramsMap = {
            "symbol": "BTC-USDT",
            "type": "MARKET",
            "side": "SELL",
            "positionSide": "LONG",
            "price": 0.0,
            "quantity": venta,
            "stopPrice": 0.0,
            "timestamp": timestamp,
            "recvWindow": 0,
            "timeInForce": ""
        }
        paramsStr = praseParam(paramsMap)
        response_text = send_request(method, path, paramsStr, payload)
        print("Respuesta de la venta:", response_text)
    else:
        print("No se pudo obtener el valor de la posición")
