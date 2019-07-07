import os
import ujson
import ssl, requests

from datetime import date
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


today = date.today()
today = today.strftime("%d_%m_%Y")

with open('lastdate.txt', 'w') as f:
    f.write(today)

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

        resp_json = r.json()
        if len(resp_json) == 0:
            print('no more data, break')
            return False 

        if remove_exist and os.path.exists(filepath):
            os.remove(filepath) 
            print(filepath, 'removed & created')
        
        with open(filepath, 'a') as f:
            for item in resp_json:
                ujson.dump(item, f, ensure_ascii=False)
                f.write('\n')
            print(filepath, 'appended', 'from', offset, 'limit', limit)

        return True


if __name__ == '__main__':
    tags = [
        'users', 
        'binders', 
        'posts', 
        'photos', 
        'comments', 
        'likes', 
        'shares',
        'managements', # [TODO] only once
    ]

    # [TODO] 2019/07/07 일 만나면 break 하는 로직. (마지막 데이터 갖고 온 것 기준 중지)
    
    tag = tags[7]
    LIMIT = 100
    for offset in range(0, 30000, LIMIT):
        remove_exist = False 
        if offset == 0:
            remove_exist = True 
        cont = request_https('https://feeeld.com/get_{}'.format(tag), offset, LIMIT, tag, remove_exist=remove_exist, pw=pw)
        if not cont:
            break
        if tag == 'managements':
            break
