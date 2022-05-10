import ssl
import requests

from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from requests import Session
from bs4 import BeautifulSoup as BS
from ssl_new import TlsAdapter
import random

class Proxy_get:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        self.resp = requests.get(self.url)
        self.http = str(self.resp.text).split('\n')
        self.session = requests.session()
        self.adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        self.session.mount("https://", self.adapter)

    def get_session(self):
        return self.session, self.http




#session = Session()

#response = session.get("https://www.avito.ru/rossiya/predlozheniya_uslug?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&p=2&q=%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0", proxies={
 #   'http': http[random.randint(0, len(http) - 1)]})
#print(response.status_code)