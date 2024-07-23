import urllib.request
import json
import time
from threading import Lock
from settings import settings

class TokenManager:
    def __init__(self):
        self._cached_token = None
        self._token_expiry = 0
        self._lock = Lock()

    def generate_token(self):
        obj = {'APIPassword': settings.API_PASSWORD}
        json_data = json.dumps(obj).encode('utf8')
        req = urllib.request.Request(f"{settings.API_URL}/token", data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req) as res:
                content = json.loads(res.read())
                print(content)  # デバッグ用
                token_value = content.get('Token')
                if token_value:
                    self._token_expiry = time.time() + 3600  # 仮に1時間の有効期限を設定
                    return token_value
                else:
                    raise ValueError("Token not found in response")
        except urllib.error.URLError as e:
            print(f"Network error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error generating token: {e}")
            raise

    def get_token(self):
        with self._lock:
            if self._cached_token is None or time.time() > self._token_expiry:
                self._cached_token = self.generate_token()
            return self._cached_token

token_manager = TokenManager()
get_token = token_manager.get_token
