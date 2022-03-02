from django.shortcuts import get_object_or_404
from django.db.models.query_utils import Q

from rottenshoe_drf.serializer import CoD_Serializer, MyPageSerializer, MyTokenObtainPairSerializer, SneakerSerializer,IndexSerializer, CreateUserSerializer,CommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import JSONParser

from .models import *
from .token import *
from .recommend import *

from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
'''
1)메인페이지
2)상세페이지
3)로그인, 로그아웃 - jwt 사용
4)댓글 작성 및 관리(삭제,수정)
5)회원가입
6)평가 (Cop or Drop)
7)마이페이지 요청 및 회원 정보 수정
8)검색 요청
'''


class IndexAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="메인페이지 데이터 요청",
        tags=['main']
    )
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_percent') # 추후 로직 변경(조회수 / 최근 유저의 조회량/ 점수 종합)
        newList = IndexSerializer(newList, many = True)
        hotList = IndexSerializer(hotList, many = True)
        return Response({'newList' : newList.data[:5],'hotList':hotList.data[:5]}, status.HTTP_200_OK)

#더보기 작업 분할
class ListAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="카테고리별 확장 데이터 요청",
        tags = ['main_expand'],
    )
    def get(self,req,category):
        if category == 'new':
            newList = SneakerSerializer(Sneakers.objects.all().order_by('-retail_date'), many = True)
            return Response(newList.data,status.HTTP_200_OK)
        #추후 로직 변경(조회수 / 최근 유저의 조회량/ 점수 종합)
        elif category == 'hot':
            hotList = SneakerSerializer(Sneakers.objects.all().order_by('-cop_percent'), many = True)
            return Response(hotList.data,status.HTTP_200_OK)

class CommentAPIView(APIView):
    @swagger_auto_schema(
        operation_description="댓글 추가",
        tags = ['comment'],
        request_body=CommentSerializer
    )
    def post(self,req):
        s_id = req.data['id']
        board = get_object_or_404(Sneakers,id = s_id)

        u_id = decoder(req.headers['Access-Token'])['user_id']
        user = get_object_or_404(User, id = u_id)

        comment = req.data['comment']

        Comment(
            board_id = board,
            user_id = user,
            comment = comment
        ).save()

        return Response(None,status = status.HTTP_202_ACCEPTED)

    #댓글 수정(update)
    @swagger_auto_schema(
        operation_description="댓글 수정",
        tags = ['comment'],
        request_body=CommentSerializer
    )
    def put(self,req):
        
        board_id = req.data['board_id']
        u_id = decoder(req.headers['Access-Token'])['user_id']
        comment = req.data['comment']
        try:
            comment_instance = get_object_or_404(Comment,board_id=board_id,user_id = u_id)
            #serialize 사용 update 방식 주어진 instance와 변경될 데이터를 보내주어 변경 후 저장.
            serializer = CommentSerializer(comment_instance,data = {'comment' : comment})
        except Comment.DoesNotExist:
            return Response({'error' : '실행 될 수 없는 요청입니다.'}, status = status.HTTP_404_NOT_FOUND)
        return Response(None,status=status.HTTP_202_ACCEPTED)
    
    #댓글 삭제(delete)
    @swagger_auto_schema(
        operation_description="댓글 삭제",
        tags = ['comment'],
        request_body=CommentSerializer
    )
    def delete(self,req):
        board_id = req.data['board_id']
        u_id = decoder(req.headers['Access-Token'])['user_id']
        try:
            comment_instance = get_object_or_404(Comment,board_id=board_id,user_id = u_id)
            comment_instance.delete()
        except Comment.DoesNotExist:
            return Response({'error' : '존재하지 않는 댓글입니다.'}, status = status.HTTP_404_NOT_FOUND)
        
class ObtainTokenPairWithNickname(TokenObtainPairView):
    permission_classes = (AllowAny,) 

    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="회원 가입",
        tags = ['register'],
        request_body=CreateUserSerializer
    )
    def post(self,req):
        data = JSONParser().parse(req)
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = 201)
        return Response(status=400)

class DetailAPIView(APIView):
    @swagger_auto_schema(
        operation_description="상세페이지",
        tags = ['detail_page'],
    )
    def get(self,req,id):

        sneaker = Sneakers.objects.get(id = id)
        sneaker_data = sneaker
        board = SneakerSerializer(sneaker)
        #필요한 데이터만 뽑아서 오기 values_list
        #객체 자체를 보내줘야 콜업 가능.
        s_features  = SneakerFeatures.objects.filter(sneaker=sneaker_data)
        #추천리스트 get
        #전체에서 자신을 뺀 나머지 스니커 데이터와 비교하여 가장 비슷한 리스트 5개 콜업.
        recommand_data = get_cos_similar(s_features)[:5]

        #토큰 유무 확인
        try:
            u_id = decoder(req.headers['Access-Token'])['user_id']
        except AssertionError:
            u_id = None
            return Response(status = 200)
        #토큰 값이 있을 때(로그인 하고 접근 했을 때)
        if u_id is not None:
            user = get_object_or_404(User,id=u_id)
            #조회수 카운트
            sneaker.update_view_count
            #유저 접속 기록 데이터 저장
            UserMovementOfViews.objects.create(user_id = user,sneaker_id = sneaker)
            #현 유저가 현재 게시판에서 평가 내역 확인
            user_cod = CopOrDrop.objects.get(user_id = user, board_id = sneaker)
            if user_cod:
                user_cod = CoD_Serializer(user_cod)
            else:
                user_cod = None
        #로그인 없이 접근 했을 때
        else:
            sneaker.update_view_count
    
        return Response({'board': board.data}, status = status.HTTP_200_OK)
class CopOrDropAPIView(APIView):
    #cop or drop 평가 저장
    @swagger_auto_schema(
        operation_description="신발 평가 Cop Or Drop",
        tags = ['CoD'],
        request_body=CoD_Serializer
    )
    def post(self,req):
        #로그인 여부 확인
        try:
            u_id = decoder(req.headers['Access-Token'])['user_id']
        except KeyError:
            return Response({"response" : "토큰 값 없음"},status=status.HTTP_401_UNAUTHORIZED)
            
        s_id = req.data['id']
        u_id = decoder(req.headers['Access-Token'])['user_id']

        user = get_object_or_404(User,id = u_id)
        board = get_object_or_404(Sneakers, id = s_id)

        # 평가로직
        board.total_count += 1

        if bool(req.data['cop']):
            board.cop_count += 1
            CopOrDrop.objects.create(user_id = user, board_id = board, choice = True)
        else:
            CopOrDrop.objects.create(user_id = user, board_id = board, choice = False)

        board.cop_percent = board.cop_count / board.total_count
        board.save()
        return Response(None,status=status.HTTP_201_CREATED)


class MypageAPIView(APIView):
    @swagger_auto_schema(
        operation_description="마이페이지 요청",
        tags = ['MyPage'],
        request_body=MyPageSerializer
    )
    def get(self,req):
        #접근하려고 할 때 토큰이 없으면 로그인 요청
        try:
            u_id = decoder(req.headers['Access-Token'])['user_id']
        except KeyError:
            return Response({"response" : "토큰 값 없음"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = get_object_or_404(User,id = u_id)
            return Response(MyPageSerializer(user),status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    @swagger_auto_schema(
        operation_description="마이페이지 수정",
        tags = ['MyPage'],
        request_body=MyPageSerializer
    )
    def post(self,req):
        u_id = decoder(req.headers['Access-Token'])['user_id']

        user = get_object_or_404(User,id = u_id)
        data = {'nickname' : req.get['nickname']}

        MyPageSerializer(user,data=data)


class SearchAPIView(APIView):
    @swagger_auto_schema(
        operation_description='검색 기능',
        tags = ['search']
    )
    def get(self,keyword):
        result = []
        word_list = keyword.split(" ")
        keyword_list = [k.keyword for k in Keyword.objects.all()]

        #기존은 단어값마다 요청을 보냈지만 이를 q객체를 이용하여 한번의 쿼리로 읽어오게 함.
        q = Q()
        for word in word_list:
            if word in keyword_list:
                model_number_list = list(Keyword.objects.filter(keyword=word))
                result += [Sneakers.objects.get(model_number = s.sneaker_id) for s in model_number_list]
            else:
                q.add(Q(sneaker_name__icontains = word)| 
                    Q(brand__icontains = word) |
                    Q(sneaker_name_ko__icontains = word))
        result = list(Sneakers.objects.filter(q).distinct().order_by('views'))

        context = {'result' : result, 'keyword':keyword}
        #검색시각과 키워드를 저장하여 추후 계절별이나 날씨별 추천에 사용하려고 함.
        SearchRequest.objects.create(keyword = keyword, request_time = datetime.datetime.now())
        return Response(context,status = status.HTTP_200_OK)