import os
import ujson
import datetime
import ssl, requests

from datetime import date, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


today = date.today()
today_str = today.strftime("%Y-%m-%d")


last_date = None
with open('last_date.txt') as f:
    last_date = datetime.datetime.strptime(f.read().strip(), "%Y-%m-%d").date()
    thres_date = last_date - timedelta(days=1)
    print(str(last_date), str(thres_date))

pw = os.environ['PW']
print('password:', pw)


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
        filepath = './data/{}_{}.txt'.format(tag, today_str)

        resp_json = r.json()
        if len(resp_json) == 0:
            print('no more data, break')
            return False 

        if remove_exist and os.path.exists(filepath):
            os.remove(filepath) 
            print(filepath, 'removed & created')
        
        with open(filepath, 'a') as f:
            for item in resp_json:
                doc_time = datetime.datetime.strptime(item['updated_at'][:len('2018-01-02')], "%Y-%m-%d")
                doc_time_unix = int(doc_time.strftime('%s'))
                thres_time_unix = int(thres_date.strftime('%s'))
                if doc_time_unix < thres_time_unix:
                    return False
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
        # 'managements', # [TODO] only once
    ]

    download = False 

    if download:
      for tag in tags:
          LIMIT = 100
          for offset in range(0, 30000, LIMIT):
              remove_exist = False 
              if offset == 0:
                  remove_exist = True 
              cont = request_https('https://feeeld.com/get_{}'.format(tag), offset, LIMIT, tag, remove_exist=remove_exist, pw=pw)
              if not cont:
                  break

      with open('last_date.txt', 'w') as f:
          f.write(today_str)
    
    # migration
    from convert_user import migrate_user
    from convert_binder import migrate_binder
    from convert_post_with_photo import migrate_post_with_photo
    from convert_comment import migrate_comment
    from convert_share import migrate_share
    from convert_like import migrate_like


    today_str = '2019-09-24' # [TODO] 임시


    """
    [1] 유저 넣기
    """
    migrate_user('./data/{}_{}.txt'.format('users', today_str))
    
    """
    [2] 바인더 넣기
    binder 넣고 UserId 필드를 old 값을 참조해 채우기
    (new db에선 user와 binder가 many to many 임)
    oldUserId가 일치하는 user객체를 가져와서 user.addBinder로 연결
    """
    migrate_binder('./data/{}_{}.txt'.format('binders', today_str))

    """
    [3] 포스트 넣기
    (user에 belongsTo, binder belongsTo 관계)
    oldUserId가 현재 id가져와서 생성시 활용 
      User.find({where: { oldUserId: ...}).id
    binderId 도 마찬가지

    """
    post_filename = './data/{}_{}.txt'.format('posts', today_str)
    photo_filename = './data/{}_{}.txt'.format('photos', today_str)
    migrate_post_with_photo(post_filename, photo_filename)

    """
    [4] comment 넣기
    (user에 belongsTo, post에 belongsTo 관계)
      oldUserId로 현재 id가져와서 생성시 활용 
      oldPostId로 현재 id가져와서 생성시 활용 
    """
    migrate_comment('./data/{}_{}.txt'.format('comments', today_str))

    """
    [5] share 넣기
    유저 아이디, 포스트 아이디만 처리하면 됨
    """
    migrate_share('./data/{}_{}.txt'.format('shares', today_str))

    """
    [6] like 넣기
    유저 아이디, 포스트 아이디만 처리하면 됨
    """
    migrate_like('./data/{}_{}.txt'.format('likes', today_str))
