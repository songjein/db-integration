import ujson
import requests

'''
{
'id': 64, 
'post_id': 54, 
'body': '아..', 
'user_id': 1, 
'created_at': '2016-03-21T01:53:21.000+09:00', 
'updated_at': '2016-03-21T01:53:21.000+09:00'}
'''
with open('comments.json') as f:
	for line in f:
		comment = ujson.loads(line)
		oldId = comment['id']
		oldPostId = comment['post_id']
		oldUserId = comment['user_id']
		body = comment['body']
		createdAt = comment['created_at']

		comment_data = {
			'oldId': oldId,
			'oldPostId': oldPostId,
			'oldUserId': oldUserId,
			'body': body,
			'createdAt': createdAt
		}

		API = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com:3000/comment/integrate'

		res = requests.post(API, data=comment_data)
		print(res.json())

