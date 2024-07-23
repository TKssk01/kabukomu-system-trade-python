import requests
import logging
from settings import settings

# ロガーを設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def send_order(token, action, quantity, price):
    url = f"{settings.API_URL}/sendorder"
    headers = {
        "X-API-KEY": token,
        "Content-Type": "application/json"
    }
    data = {
        "Password": '1995tAkA@@',
        "Symbol": settings.SYMBOLS[0],  # 使用する銘柄
        "Exchange": 1,
        "SecurityType": 1,
        "Side": '2' if action == "BUY" else '1',
        "CashMargin": 1,
        "DelivType": 2,
        "FundType": "AA",
        "AccountType": 2,
        "Qty": quantity,
        "FrontOrderType": 20,
        "Price": price,
        "ExpireDay": 0,
        "ReverseLimitOrder": {
            "TriggerSec": 3,
            "TriggerPrice": 1600,
            "UnderOver": 2,
            "AfterHitOrderType": 1,
            "AfterHitPrice": 0
        }
    }
    logger.info(f"Sending order to {url} with headers {headers} and data {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response content: {response.content}")
        logger.error(f"Request URL: {url}")
        logger.error(f"Request headers: {headers}")
        logger.error(f"Request body: {data}")
        raise
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        raise
