import ujson
import requests


ROOT = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com'


def migrate_like(filepath):
  with open(filepath) as f:
    for line in f:
      like = ujson.loads(line)

      oldUserId = like['user_id']
      oldPostId = like['post_id']

      createdAt = like['created_at']

      binder_data = {
        'oldUserId': oldUserId,
        'oldPostId': oldPostId,
        'createdAt': createdAt,
      }

      API = '{}:3000/like/integrate'.format(ROOT)

      res = requests.post(API, data=binder_data)
      try: 
        print(res.json())
      except Exception as e:
        print(e)
        print(binder_data)
        print(res)

'''
{"id":7644,"post_id":17399,"user_id":4929,"created_at":"2019-09-24T15:09:01.000+09:00","updated_at":"2019-09-24T15:09:01.000+09:00"}
'''
