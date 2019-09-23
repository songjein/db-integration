import ujson
import requests

# camel case for node js

# [TODO] password는 안옮길 예정. 
# 기존 서비스에서 새로운 서비스로 비밀번호 변경 요청하게끔 만들자


def migrate_user(filepath): 
  with open(filepath) as f:
    for line in f:
      user = ujson.loads(line)

      oldId = user['id']
      snsId = user['uid']

      email = user['email']  # nullable ; none

      nick = user['name']
      if nick is None:
        nick = '이름없음'
      
      #nick = user['nickname']
      #if nick is None:
      #  nick = name

      memo = user['intro']
      if memo is None:
        memo = ''
        
      company = user['company']
      provider = user['provider']

      profileImage = user['image_url'] # 소셜 유저일 경우 image_url이 채워짐
      if profileImage is None:
        profileImage = user['photo']['url']
        if profileImage == 'default.png':
          profileImage = '/user_default.png'

      createdAt = user['created_at']
      
      if provider is None  and user['uid'] != None and profileImage and user['password'] is None and "graph.facebook" in profileImage :
        provider = 'facebook'

      if provider is None and user['password'] is None:
        print('@@exception', user)
        break

      if provider is None and user['uid'] is not None:
        print('###exception', user)
        break

      if provider is None:
        provider = 'local'
      
      user_data = {
        'oldId': oldId,
        'snsId': snsId,
        'email': email,
        'nick': nick,
        'company': company,
        'provider': provider,
        'profileImage': profileImage,
        'memo': memo,
        'createdAt': createdAt
      }
      print(user_data)

      API = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com:3000/user/integrate'
      
      res = requests.post(API, data=user_data)
      print(res.json())


#from collections import Counter
#print (Counter(providers))
"""
Counter({'facebook': 2858, None: 1580, 'google_oauth2': 289})
"""

