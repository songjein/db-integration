import ujson
import requests


ROOT = 'http://ec2-54-180-96-29.ap-northeast-2.compute.amazonaws.com'


def migrate_post_with_photo(post_filename, photo_filename):
  f_post = open(post_filename)
  f_photo = open(photo_filename)

  posts = [] 
  photos = [] 
  post_dict = {}
  '''
  {"id":16814,"title":"실내 인테리어 상세뷰","content":"","created_at":"2018-11-16T22:59:25.000+09:00","updated_at":"2018-11-16T22:59:25.000+09:00","user_id":4343,"project_id":null,"post_type":1,"is_secret":false,"view_count":0,"challenge_id":null,"tag_list":[]}
  '''
  skip_cnt = 0
  for line in f_post:
    post = ujson.loads(line)
    post_id = post['id']
    post_dict[post_id] = post
    post_dict[post_id]['imgList'] = []
    post_dict[post_id]['captionList'] = []

  for line in f_photo:
    photo = ujson.loads(line)
    post_id = photo['post_id']
    img_url = photo['image']['url']
    caption = photo['caption']
    if caption is None:
      caption = ''
    
    if post_id not in post_dict:
      # print('deleted post', post_id)
      continue

    post_dict[post_id]['imgList'].append(img_url)
    post_dict[post_id]['captionList'].append(caption)	

  for idx, key in enumerate(post_dict.keys()):
    post = post_dict[key]

    if post['post_type'] == 1 and len(post['content']) == 0 and len(post['imgList']) == 0:
      skip_cnt += 1
      continue

    oldId = post['id']
    oldUserId = post['user_id']
    oldBinderId = post['project_id']

    title = post['title']
    content = post['content']
    imgList = post['imgList']
    captionList = post['captionList']
    
    tagList = post['tag_list']

    isSecret = post['is_secret']
    viewCount = post['view_count']

    createdAt = post['created_at']

    SEP = '%#@#@%'

    post_data = {
      'oldId': oldId,
      'oldUserId': oldUserId,
      'oldBinderId': oldBinderId,
      'title': title,
      'content': content,
      'imgList': (SEP).join(imgList),
      'captionList': (SEP).join(captionList),
      'isSecret': isSecret,
      'viewCount': viewCount,
      'createdAt': createdAt,
      'tagList': (SEP).join(tagList),
    }	

    if post['post_type'] == 2:
      link = post['link']
      if link == None:
        skip_cnt += 1
        continue
      post_data['imgList'] = link['image_url']
      post_data['captionList'] = '출처: <a href="' + link['link_url'] + '">' + link['link_title'] + '</a>'

    API = '{}:3000/post/integrate'.format(ROOT)

    if len(post['title']) == 0 and len(post['content']) == 0 and len(post['imgList']) == 0:
      skip_cnt += 1
      continue

    res = requests.post(API, data=post_data)
    print(res.json())

  print('skip cnt: {}'.format(skip_cnt))
  f_post.close()
  f_photo.close()

"""
'id': 17208, 
'title': "2018년 제8회 한국리모델링 건축대전 입상 'Little Forest' - 한경대학교 건축학과 이소라", 
'content': ', 
'created_at': '2019-05-12T01:10:58.000+09:00', 
'updated_at': '2019-05-19T19:05:14.000+09:00', 
'user_id': 4316, 'project_id': None, 'post_type': 1, 
"""
