# [NOTICE]
- 6월/6일 - 오후7:14분
- Counter({'facebook': 2858, None: 1604, 'google_oauth2': 289})
- posts 15438개 중 183개 스킵됨 

# [TODO]
- like 가져오기
- share 가져오기
- 작업 순서 참고 자동화

# [작업 순서]
- user을 가장 먼저 넣고

- binder 넣고 UserId 필드를 old 값을 참조해 채우기
	- (new db에선 user와 binder가 many to many 임)
	- oldUserId가 일치하는 user객체를 가져와서 user.addBinder로 연결

- posts 넣기
	- (user에 belongsTo, binder belongsTo 관계)
	- oldUserId가 현재 id가져와서 생성시 활용 
		- User.find({where: { oldUserId: ...}).id
	- binderId 도 마찬가지

- comment 넣기
	- (user에 belongsTo, post에 belongsTo 관계)
	- oldUserId로 현재 id가져와서 생성시 활용 
	- oldPostId로 현재 id가져와서 생성시 활용 


