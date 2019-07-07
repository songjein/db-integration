import ujson
import requests

# camel case for node js

# [TODO] password는 안옮길 예정. 
# 기존 서비스에서 새로운 서비스로 비밀번호 변경 요청하게끔 만들자

"""
	2019/06/02 4727개 성공적으로 삽입
	
	그냥 실행 시키면 됨
	중간 부터 실행 할 경우 continue 조건 추가
"""
providers = []
with open('users.json') as f:
	for line in f:
		user = ujson.loads(line)

		oldId = user['id']
		snsId = user['uid']

		email = user['email']  # nullable ; none

		name = user['name']
		nick = user['nickname']
		if name == None:
			name = '이름없음'
		if nick == None:
			nick = name
			
		company = user['company']
		provider = user['provider']

		profileImage = user['image_url'] # 소셜 유저일 경우 image_url이 채워짐
		if profileImage == None:
			profileImage = user['photo']['url']
			if profileImage == 'default.png':
				profileImage = '/user_default.png'

		createdAt = user['created_at']
		
		if provider == None  and user['uid'] != None and profileImage and user['password'] == None and "graph.facebook" in profileImage :
			provider = 'facebook'

		if provider == None and user['password'] == None:
			print('exception', user)

		if provider == None and user['uid'] != None:
			print('exception', user)
		
		user_data = {
			'oldId': oldId,
			'snsId': snsId,
			'email': email,
			'nick': nick,
			'company': company,
			'provider': provider,
			'profileImage': profileImage,
			'createdAt': createdAt
		}

		API = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com:3000/user/integrate'
		
		#skip_to = 2543
		#if oldId < skip_to:
		#	continue 

		res = requests.post(API, data=user_data)
		print(res.json())

		providers.append(provider)


from collections import Counter
print (Counter(providers))

"""
Counter({'facebook': 2858, None: 1580, 'google_oauth2': 289})
"""

