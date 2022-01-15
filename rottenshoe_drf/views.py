from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

from rottenshoe_drf.serializer import SneakerSerializer

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
        
class IndexAPIView(APIView):
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_count') # 점수순 => order_by 이용하려면 속성값 하나 추가 ?
        newList = SneakerSerializer(newList, many = True)
        hotList = SneakerSerializer(hotList, many = True)

        if req.data['mode'] == 'newFull':
            return Response(newList.data,200)
        elif req.data['mode'] == 'hotFull':
            return Response(newList.data,200)

        # 더보기 클릭 시 전체 리스트 전송(newList, hotList 따로 운용)
        return Response([newList.data[:5],hotList.data[:5]], 200)

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
        board = get_object_or_404(Sneakers, id = s_id)
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
