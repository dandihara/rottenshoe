# rottenshoe

-> 로튼토마토를 모티브로 만든 서비스입니다. 
  신발을 보고 이 아이템의 대한 각자의 생각을 작성하여, 현재 뜨는 아이템이 무엇인지 판단 내릴 수 있고, 신발을 이용한 패션 코디사진을 서로에게 보여 줄 수 있는 스니커즈 씬 전문 커뮤니티를 만들고자 하였습니다.

# requirement.txt
-asgiref==3.4.1

-certifi==2021.10.8

-cffi==1.15.0

-charset-normalizer==2.0.10

-cryptography==36.0.1

-defusedxml==0.7.1

-Django==4.0.1

-django-allauth==0.47.0

-django-cors-headers==3.11.0

-django-rest-auth==0.9.5

-djangorestframework==3.13.1

-djangorestframework-simplejwt==5.0.0

-idna==3.3

-mysqlclient==2.1.0

-oauthlib==3.1.1

-Pillow==9.0.0

-pycparser==2.21

-PyJWT==2.3.0

-python3-openid==3.2.0

-pytz==2021.3

-requests==2.27.1

-requests-oauthlib==1.3.0

-six==1.16.0

-sqlparse==0.4.2

-tzdata==2021.5

-urllib3==1.26.8


# 버전별 목표
- v1 
1) 신발 검색(대/소문자, 키워드, 영어 한글 혼용 가능)
2) 유저 평가 (댓글, 점수)
=>![drf](https://user-images.githubusercontent.com/23503161/149620668-7c956ab1-326b-4081-a618-45e60b809856.PNG)
 app 추가 (DRF) / 화면단을 내부에서 따로 주는 것만 하다가 백과 화면단을 따로 구현하기 위하여 Django Rest Framework를 이용한 백에 집중하도록 api url 을 이용하여 따로 만들기 시작
 
 - drf 사용이유 : serializer 라이브러리 같은 api에 적용할 때, 필요한 내용을 좀 더 편리하게 구비되었으며 postman대용으로 간단한 테스트를 적용하여 확인할 수 있다는 장점이 있어서 선택.
 
- v2
1) 룩북 페이지(sns)
2) 중고 거래 추가(개인간 거래 시, 인증 시스템 구상)

- v3
1) 신발 추천 시스템 (아이템 간 유사도 검색)


backend : django
frontend : vanilla js / html+css



# v1 ERD 구상도
- ERD 페이지 https://www.erdcloud.com/d/vY5yNp9JGZtmAvwsM
![v1 erd](https://user-images.githubusercontent.com/23503161/149963194-57d31ad2-e558-47fe-ae98-240bf763c3e7.PNG)

- Sneakers : ScoreBoard,Comments,CopOrDrop = 1:N
- User : ScoreBoard,Comments,CopOrDrop = 1:N
- Sneakers : Keyword = 1:N

- 키워드 테이블을 따로 둔 이유 :
  #선택지 
  - 1) 신발 테이블(Snaeker)에 속성값으로 둔다. 
  - 2) 테이블을 따로 두어서 관리한다.

  간단하게만 생각하면 테이블에 엮어서 쓰는 걸 생각했으나 기본으로 돌아가 생각해본 결과는 2번이었다.
  1번으로 갈 경우, 제일 기본적인 제1정규형을 범할 수가 있기에 그랬다.

 2번으로 선택하고 나서 생각한 것은 검색을 요청하는 방향이었다. 일반적인 모델명을 한글로 하는 키워드는 현재 신발 속성값 중 한글 타이틀과 icontains를 사용하여 접근하는 것이 디비 요청 수가 적다고 생각됐지만, 특별 키워드는 말 그대로 별칭같은 것이기에 생길때마다 운영자가 따로 처리하는 것이 맞다고 판단되어 다음과 같이 테이블을 따로 구현 해 두었다.


# URL(api)

- "api/" => 메인페이지 [GET]

- "api/(options)" => 메인페이지 확장형
                      [GET] category => hot or new (키워드에 따른 리스트 변동)

- "api/detail/(s_id)" => 상세페이지
                      [GET] id => 신발 데이터 인덱스
                      header => access-token(not required)

- "api/register => 회원가입 [POST]
                    body {
                      email, password, confirme_password, nickname
                    }

- "api/cop/ => 평가 url [POST]
                    headers = { Access-Token : "access-token"}
                    body{
                      id = 게시판 id(신발 index),
                      cop = 선택지(boolean)
                    }

- "token/obtain" => jwt token 요청 및 생성 [POST] 
                body{ 
                  email, password 
                  }
                  
- "token/refresh" => jwt token 만료(Unauthorized or 401 error) 토큰 재반환 요청[POST]
                  body {
                    refresh : refresh_token
                  }
- "api/search/(keyword) => 검색 요청 [GET]

# 생각들...
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
 
 - 생각하는 방향의 1순위는 코드의 가시성을 우선적으로 보려고 함.사용자 입장에선 큰 차이가 있지 않을 것이라 판단하여 그렇다.
 - 평가 테이블 (CopOrDrop) 추가
 - Sneakers 테이블 속성값 추가(cop_percent) 

21-01-16
  - 핫하다는 컨텐츠를 어떻게 구할 것인가 ? 조회수 값을 추가해볼 생각. detail에서 유저가 들어온다면 조회수가 늘어나도록 동기 ? 비동기처리 ??

21-01-18
  - 일단 조회수는 동기로 처리하고 유저의 성향을 분석하기 위한 데이터 테이블 추가하게 됨(게시판 접근 시 저장) 시간과 어떤 게시판인지 저장되어 유저의 성향을 분석할 수 있을 듯.

21-01-23
  - 검색 로직 확인 -> 크림과 비슷한 면이 있으나 다른 점이 발견 / 현재 띄어쓰기 기준으로 키워드를 끊어 데이터를 가져오는데 띄어쓰기가 들어간 키워드도 있음을 발견.

21-01-27
  - swagger 코드 추가 -> 명세서 제작 편의성을 위해서 제작 
  - ![swagger 추가](https://user-images.githubusercontent.com/23503161/151375595-782cd4a2-44d3-4b73-9d93-094d917a23d2.PNG)

21-01-29
  - rest_framework.permission 이용해 api 접근 가능 여부를 생각해 볼 만 할 듯. (doc & 구글링 이용)

21-01-30
 - drf validation을 꼭 써야하는가 ?? 예시 로직이 일반적인 orm 사용과 비교했을 때 코드양은 줄지라도 기존 orm 코드로 썼을 때가 가독성이 좋다고 생각이 들음.

21-02-04
- hot list 쿼리 셋업 => 유저 접근 기록 테이블 사용 (기간 중에 조회된 리스트 사용) + 검색 요청도 테이블로 저장 해 둬서 이용
- 검색 요청 테이블 추가
- 첫번째 추천은 협업 필터링 사용 예정(유클리드 / 현 신발 데이터에 신발끼리 비슷할 수 있는 키워드나 값 추가 (boolean))
- static 파일 세팅(배포세팅) / 유저 값 유무에 따라 api 로직 재 설정

21-02-05
- 배포 세팅(static파일 부재로 인한 화면 꺠짐)

21-02-06
- nginx에 대한 고찰 필요성 느낌 => upstream / server(도메인 주소를 얻어야만 사용 가능한 건가 ?)

21-02-12
- 컨텐츠 기반 필터링을 선정 => 현재, 유저가 접근한 기록을 이용하여 진행..
-  feature들을 생각해야함(브랜드, 컬러, 편의성, 가격, 경량성, 착화감 등등) => 착화감이나 편의성은 일단 따로 테이블을 만들려고 함.

21-02-14
- 유클리디안 / 코사인 유사도 둘 중에 하나 (로직이 간단하며 착화감 등 항목들이 숫자 값으로 이루어져 적용이 가능하다고 판단함.)
- DB Index의 여부에 따른 쿼리 시간 확인 -> 이를 이용하는 방식을 이용하여 기존에 했던 데이터를 만드는 방식이 아닌 실시간으로 할 수 있는 방식을 찾아보도록 하려고 함. 
- 인덱스를 사용하려면 유저 자체보단 스니커즈끼리의 유사도를 이용하는 게 맞을듯.
- 
21-02-15
- 유클리디안보다 코사인 유사도가 좀 더 값을 도출 했을 때 한 눈에 잡히긴 함.
- 중복된 값이 없기에 둘 다 사용 가능인 상황 ..

21-02-17
- 적용 후 테스트 한 이후로 db연결에서 문제점 발생 - 로직상에서 문제인지, 설정상의 문제인지 확인해봐야 할듯.
- logger 적용해야 편안하게 시작할듯 .. 담번부턴 애초에 logger를 넣고 시작하려고 함.


21-02-19
- 검색어 띄어쓰기 + 형태소 분리 로직 염두.

21-02-22
- 검색 로직 변화 -> 단어별로 요청을 한번에 보내는것으로 (Q라이브러리) 사용. -> DB요청을 굳이 단어별로 보내야하나에서 생각을 얻게 됨(어느 게임회사의 DB의 부하를 주지 않기 위해 몇분간의 내용을 모아서 한번에 보내어 DB에 저장하는 것을 들으면서 생각해보게 됨.)

21-02-26
- 유사도 로직 문제 발생 -> orm을 뜯어봐야할듯.

21-03-01
- logger 오류 해결 / drf 내부 viewset, router 등의 내용을 다시 정리하는 시간을 가짐.

21-03-07
-aws 프리티어 db로 변경 -> maria db는 프리티어가 아님.

21-03-16
- 버전2 부터는 fastapi로 ?? django의 단점이 보이기 시작.. -> 너무나 많은 설정들이 있다보니 쓸모없는 코드가 너무나 많이 발생.
