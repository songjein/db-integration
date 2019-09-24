import ujson
import requests


ROOT = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com'


def migrate_share(filepath):
  with open(filepath) as f:
    for line in f:
      share = ujson.loads(line)

      oldUserId = share['user_id']
      oldPostId = share['post_id']

      createdAt = share['created_at']

      binder_data = {
        'oldUserId': oldUserId,
        'oldPostId': oldPostId,
        'createdAt': createdAt,
      }

      API = '{}:3000/share/integrate'.format(ROOT)

      res = requests.post(API, data=binder_data)
      print(res.json())

'''
{"id":1913,"user_id":4991,"post_id":774,"created_at":"2019-09-07T21:04:34.000+09:00","updated_at":"2019-09-07T21:04:34.000+09:00"}
'''
