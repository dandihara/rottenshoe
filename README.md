# rottenshoe

-> 로튼토마토를 모티브로 만든 서비스입니다. 
  신발을 보고 이것의 대한 각자의 평론을 하며 현재 뜨는 아이템이 무엇인지 판단 내릴 수 있고, 신발을 이용한 패션 코디등을 서로에게 보여주며 스니커즈 씬 전문 커뮤니티를 만들고자 하였습니다.

# require.txt
- asgiref      3.4.1
- cffi         1.15.0
- cryptography 36.0.1
- Django       4.0.1
- PyJWT        2.3.0
- mysqlclient  2.1.0
- Pillow       9.0.0
- pip          20.2.3
- pycparser    2.21
- setuptools   49.2.1
- sqlparse     0.4.2
- tzdata       2021.5

# 버전별 목표
- v1 
1) 신발 검색(대/소문자, 키워드, 영어 한글 혼용 가능)
2) 유저 평가 (댓글, 점수)
=>![drf](https://user-images.githubusercontent.com/23503161/149620668-7c956ab1-326b-4081-a618-45e60b809856.PNG)
 app 추가 (DRF) / 화면단을 내부에서 따로 주는 것만 하다가 백과 화면단을 따로 구현하기 위하여 Django Rest Framework를 이용한 백에 집중하도록 api url 을 이용하여 따로 만들기 시작
 - drf 사용이유 : 일반적으로 테스트 시 postman을 사용하는 것을 좀 더 편리하게 윗 그림처럼 api를 제작하면 알아서 데이터를 읽어오는 것을 확인 할 수 있기에, 그리고 serializer가 있으므로 
 json형식을 더 일반 django보다 간편하게 구현할 수 있기에 코드가 단축 가능
- v2
1) 룩북 페이지(sns)
2) 중고 거래 추가(개인간 거래 시, 인증 시스템 구상)

- v3
1) 신발 추천 시스템 (아이템 간 유사도 검색)


backend : django
frontend : vanilla js / html+css



# v1 ERD 구상도



![v1 erd](https://user-images.githubusercontent.com/23503161/149322145-2cc8da7e-0461-45a0-9d82-ce6143749528.PNG)


- Sneakers : ScoreBoard,Comments = 1:N
- User : ScoreBoard,Comments = 1:N
- Sneakers : Keyword = 1:N

# 고민 리스트


검색에 대한 고민 - 대/소문자 , 키워드 검색 방식(키워드를 신발 테이블 속성값으로 추가하여 조회시에 이용)

대/소문자 => icontains를 사용하여 해결
한 /영 키워드 => ? ex> 범고래, 조던 이런경우는 어떻게 찾는가 ? 


- 1안 . 영어로 된 타이틀을 한글로 바꿔 속성값에 추가한다. ex> jordan 1 royal blue => 조던 1 로얄 블루
- 2안 . 키워드를 스니커즈의 인덱스를 하나의 컬럼으로 하는 테이블 작성 ex > 범고래 / dh2000 - 100(index : 16)

=> 방법 : 속성값들을 추가한다 . 문자열로 받아서 icontains 사용 , 키워드 테이블 추가하여 키워드는 따로 처리하도록 함.
 -> 키워드가 검색 된 경우 여러값이 아닌 단일값으로 검색하는 상황이 많아서 저장된 키워드가 확인이 되는 순간 그 값으로 검색을 시도하고 바로 화면에 구성되도록 
 
 
 21-01-15
 
 - 상세페이지의 post형식에 분기를 주어 평가나 댓글 저장을 할 것인가 ? 
 - 아니면 url를 따로 주어야 더 좋을것인가 ?? 
 => 생각하는 방향의 1순위는 코드의 가시성을 우선적으로 보려고 함. => 사용자 입장에선 큰 차이가 있지 않을 것이라 판단하여 그렇다.
