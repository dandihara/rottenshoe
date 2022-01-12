# rottenshoe

-> 로튼토마토를 모티브로 만든 서비스입니다. 
  신발을 보고 이것의 대한 각자의 평론을 하며 현재 뜨는 아이템이 무엇인지 판단 내릴 수 있고, 신발을 이용한 패션 코디등을 서로에게 보여주며 스니커즈 씬 전문 커뮤니티를 만들고자 하였습니다.

# require.txt
asgiref      3.4.1

cffi         1.15.0

cryptography 36.0.1

Django       4.0.1

jwt          1.3.1

mysqlclient  2.1.0

Pillow       9.0.0

pip          20.2.3

pycparser    2.21

setuptools   49.2.1

sqlparse     0.4.2

tzdata       2021.5


# 버전단위 
- v1 
1) 신발 검색(대/소문자, 키워드, 영어 한글 혼용 가능)
2) 유저 평가 (댓글, 점수)

- v2
1) 룩북 페이지(sns)
2) 중고 거래 추가(개인간 거래 시, 인증 시스템 구상)

- v3
1) 신발 추천 시스템 (아이템 간 유사도 검색)


backend : django
frontend : vanilla js / html+css



# v1 ERD 구상도

![v1 erd](https://user-images.githubusercontent.com/23503161/148891749-fffba11c-bbe0-4f70-b4c9-6581ad9579ab.PNG)


# 고민 리스트

검색에 대한 고민 - 대/소문자 , 키워드 검색 방식(키워드를 신발 테이블 속성값으로 추가하여 조회시에 이용)

대/소문자 => icontains를 사용하여 해결
한 /영 키워드 => ? ex> 범고래, 조던 이런경우는 어떻게 찾는가 ? 


- 1안 . 영어로 된 타이틀을 한글로 바꿔 속성값에 추가한다. ex> jordan 1 royal blue => 조던 1 로얄 블루
- 2안 . 키워드를 스니커즈의 인덱스를 하나의 컬럼으로 하는 테이블 작성 ex > 범고래 / dh2000 - 100(index : 16)


=> 방법 : 속성값들을 추가한다 . 문자열로 받아서 icontains 사용 , 키워드를 테이블로 만들경우 조인 발생이 자주 발생하기에 유저 수가 늘어나면 문제가 있을것이라 판단.
