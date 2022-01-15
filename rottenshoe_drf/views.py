from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

from rottenshoe_drf.serializer import SneakerSerializer,IndexSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .token import *

import json


'''
1)메인페이지
2)상세페이지
3)로그인, 로그아웃
4)댓글 작성

'''

        
#hotList 정렬 키워드 고안 필수
class IndexAPIView(APIView):
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_percent') # 점수순 => order_by 이용하려면 속성값 하나 추가 ?
        newList = IndexSerializer(newList, many = True)
        hotList = IndexSerializer(hotList, many = True)
        return Response([newList.data[:5],hotList.data[:5]], 200)

#더보기 작업 분할
class ListAPIView(APIView):
    def get(self,req,mode):
        if mode == 'newFull':
            newList = SneakerSerializer(Sneakers.objects.all().order_by('-retail_date'), many = True)
            return Response(newList.data,200)
        elif mode == 'hotFull':
            hotList = SneakerSerializer(Sneakers.objects.all().order_by('-cop_percent'), many = True)
            return Response(hotList.data,200)

class LoginAPIVIew(APIView):
    def post(self,req):
        data = json.loads(req.body.decode('utf-8'))
        client = authenticate(email = data['email'], password = data['password'])
        if client is not None:
            auth_login(req,client)
            access_token =  create_token(client.nickname,client.email,client.id)
            req.session['access_token'] = access_token

class LogoutAPIView(APIView):
    def post(self,req):
        auth_logout(req)

class CopOrDropAPIView(APIView):
    #cop or drop 평가 저장
    def post(self,req):
        s_id = req.data['id']
        u_id = decoder(req.session['access_token'])['id']
        board = get_object_or_404(Sneakers, id = s_id)
        user = get_object_or_404(User,id=u_id)
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
        return Response(target.data)

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
