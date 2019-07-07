import ujson
from collections import Counter

years = []
with open('posts.json') as pf:
	for line in pf:
		post = ujson.loads(line)
		if post['post_type'] == 2:
			continue
		years.append(post['created_at'].split('-')[0])

print(Counter(years))
