import ujson
import requests

# camel case for node js

"""
	20190602
	297개의 바인더(with UserBinder association) 성공적으로 삽입

"""

with open('projects.json') as f:
	binders = ujson.loads(f.read())
	for binder in binders:
		oldId = binder['id']
		oldUserId = binder['user_id']

		title = binder['name']
		photo = binder['photo']['url']
		if photo == 'project_default.jpg':
			photo = '/binder_default.jpg'
		desc = binder['desc']
		createdAt = binder['created_at']

		binder_data = {
			'oldId': oldId,
			'title': title,
			'oldUserId': oldUserId,
			'photo': photo,
			'desc': desc,
			'createdAt': createdAt,
		}

		API = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com:3000/binder/integrate'

		res = requests.post(API, data=binder_data)
		print(res.json())

"""
{
'id': 33, 
'name': '동사무소', 
'user_id': 11, 
'created_at': '2016-03-21T14:07:02.000+09:00', 
'updated_at': '2016-03-21T14:07:02.000+09:00', 
'photo': {'url': 'project_default.jpg', 'medium': {'url': 'project_default.jpg'}, 'thumb': {'url': 'project_default.jpg'}}, 
'desc': None
}
"""


