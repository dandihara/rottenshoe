from multiprocessing import AuthenticationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rottenshoe_drf.serializer import MyTokenObtainPairSerializer, SneakerSerializer,IndexSerializer, CreateUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .token import *

import re


'''
1)메인페이지
2)상세페이지
3)로그인, 로그아웃
4)댓글 작성
5)회원가입

'''

        
#hotList 정렬 키워드 고안 필수
class IndexAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_percent') # 점수순 => order_by 이용하려면 속성값 하나 추가 ?
        newList = IndexSerializer(newList, many = True)
        hotList = IndexSerializer(hotList, many = True)
        return Response({'newList' : newList.data[:5],'hotList':hotList.data[:5]}, 200)

#더보기 작업 분할
class ListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,req,mode):
        if mode == 'new':
            newList = SneakerSerializer(Sneakers.objects.all().order_by('-retail_date'), many = True)
            return Response(newList.data,200)
        elif mode == 'hot':
            hotList = SneakerSerializer(Sneakers.objects.all().order_by('-cop_percent'), many = True)
            return Response(hotList.data,200)

class CopOrDropAPIView(APIView):
    #cop or drop 평가 저장
    def post(self,req):
        s_id = req.data['id']
        u_id = decoder(req.session['access_token'])['id']
        board = get_object_or_404(Sneakers, id = s_id)
        # 평가로직
        board.total_count += 1
        if req.data['cop'] == 1:
            board.cop_count += 1
        board.cop_percent = board.cop_count / board.total_count
        board.save()

class DetailAPIView(APIView):
    def get(self,req,id):
        target = get_object_or_404(Sneakers,id = id)
        target = SneakerSerializer(target)
        u_id = decoder(req.session['access_token'])['id']
        user = get_object_or_404(User,id=u_id)

        try:
            user_ev = CopOrDrop.object.get(user_id = user, board_id = target)
        except CopOrDrop.DoesNotExist:
            user_ev = None
        
        return Response({'board': target.data,'evaluate':user_ev})

    def post(self,req):
        s_id = req.data['id']
        board = get_object_or_404(Sneakers,id = s_id)

        token = req.session['access_token']
        token = decoder(token)
        user = get_object_or_404(User, id = token['id'])

        comment = req.data['comment']

        Comment(
            board_id = board,
            user_id = user,
            comment = comment
        ).save()


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
            return Response({'error' : '비밀번호와 확인 비밀번호가 일치하지 않습니다.'})



class ObtainTokenPairWithNickname(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = MyTokenObtainPairSerializer