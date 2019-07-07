import os
import ujson
import ssl, requests

from datetime import date
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


today = date.today()
today = today.strftime("%d_%m_%Y")

pw = os.environ['PW']
print(pw)


class MyHttpsAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
           num_pools=connections,
           maxsize=maxsize,
           block=block,
           ssl_version=ssl.PROTOCOL_TLSv1_2
        )


def request_https(url, offset, limit, tag, remove_exist=False, pw='password'):
    with requests.Session() as s:
        s.mount('https://', MyHttpsAdapter())
        r = s.get('{}?offset={}&limit={}&pw={}'.format(url, offset, limit, pw), verify=False)
        filepath = './data/{}_{}.txt'.format(tag, today)

        if remove_exist and os.path.exists(filepath):
            os.remove(filepath) 

        with open(filepath, 'a') as f:
            for item in r.json():
                ujson.dump(item, f, ensure_ascii=False)
                f.write('\n')
            print(filepath, 'created')


if __name__ == '__main__':
    tags = [
        'posts', 
        'photos', 
        'users', 
        'binders', 
        'comments', 
        'likes', 
        'shares'
    ]
    
    tag = tags[3]
    request_https('https://feeeld.com/get_{}'.format(tag), 0, 100, tag, remove_exist=True, pw=pw)



