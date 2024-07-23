import requests
import logging
from settings import settings

# ロガーを設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def get_market_data(token, symbol):
    url = f"{settings.API_URL}/board/{symbol}"
    headers = {"X-API-KEY": token}
    logger.info(f"Requesting market data from {url} with headers {headers}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response content: {response.content}")
        logger.error(f"Request URL: {url}")
        logger.error(f"Request headers: {headers}")
        raise
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        raise
