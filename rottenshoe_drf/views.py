from django.shortcuts import get_object_or_404

from rottenshoe_drf.serializer import CoD_Serializer, MyTokenObtainPairSerializer, SneakerSerializer,IndexSerializer, CreateUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .token import *

import logging

'''
1)메인페이지
2)상세페이지
3)로그인, 로그아웃 - jwt 사용
4)댓글 작성
5)회원가입
6)평가 (Cop or Drop)

'''

        
class IndexAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_percent') # 추후 로직 변경(조회수 / 최근 유저의 조회량/ 점수 종합)
        newList = IndexSerializer(newList, many = True)
        hotList = IndexSerializer(hotList, many = True)
        return Response({'newList' : newList.data[:5],'hotList':hotList.data[:5]}, status.HTTP_200_OK)

#더보기 작업 분할
class ListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,req,category):
        if category == 'new':
            newList = SneakerSerializer(Sneakers.objects.all().order_by('-retail_date'), many = True)
            return Response(newList.data,status.HTTP_200_OK)
        #추후 로직 변경(조회수 / 최근 유저의 조회량/ 점수 종합)
        elif category == 'hot':
            hotList = SneakerSerializer(Sneakers.objects.all().order_by('-cop_percent'), many = True)
            return Response(hotList.data,status.HTTP_200_OK)

class CommentAPIView(APIView):
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


class ObtainTokenPairWithNickname(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = MyTokenObtainPairSerializer


class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,req):
        if req.data['password'] == req.data['confirm_password']:
            serializer = CreateUserSerializer(data=req.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    json = serializer.data
                    return Response(json,status=status.HTTP_201_CREATED)

            return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg' : '비밀번호와 확인 비밀번호가 일치하지 않습니다.'},
            status = status.HTTP_406_NOT_ACCEPTABLE)

class DetailAPIView(APIView):
    def get(self,req,id):
        sneaker = Sneakers.objects.get(id = id)
        board = SneakerSerializer(sneaker)
        u_id = decoder(req.headers['Access-Token'])['user_id']
        
        try:
            user = get_object_or_404(User,id=u_id)
        except User.DoesNotExist:
            return Response(None,status = status.HTTP_404_NOT_FOUND)
        #조회수 카운트
        sneaker.update_view_count
        #유저 접속 기록 데이터 저장
        UserMovementOfViews.objects.create(user_id = user,sneaker_id = sneaker)
        #현 유저가 현재 게시판에서 평가 내역 확인
        user_cod = CopOrDrop.objects.get(user_id = user, board_id = sneaker)
        print(user_cod)
        if user_cod:
            user_cod = CoD_Serializer(user_cod)
        else:
            user_cod = None
    
        return Response({'board': board.data, 'choice' : user_cod.data['choice']}, status = status.HTTP_200_OK)
class CopOrDropAPIView(APIView):
    #cop or drop 평가 저장
    def post(self,req):

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