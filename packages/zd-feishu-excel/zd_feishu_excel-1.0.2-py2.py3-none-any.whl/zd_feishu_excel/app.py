import time
import requests
from .utils import must


class App(object):
    def __init__(self, appid, secret):
        self._appid  = appid
        self._secret = secret
        self._cache  = (0, None)

    def get_tenant_access_token(self):
        now = int(time.time())
        if now < self._cache[0]:
            return self._cache[1]
        r = must(requests.post(
            'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/',
            json=dict(
                app_id=self._appid,
                app_secret=self._secret,
            ),
        ), return_data=False)
        token = r['tenant_access_token']
        self._cache = (now + r['expire'] - 1, token)
        return token
