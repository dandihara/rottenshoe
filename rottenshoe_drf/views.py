from multiprocessing import AuthenticationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rottenshoe_drf.serializer import SneakerSerializer,IndexSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
from .token import *

import re


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
        return Response({'newList' : newList.data[:5],'hotList':hotList.data[:5]}, 200)

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
        email = req.data['email']
        password = req.data['password']

        user = User.objects.get(email = email)

        if user is None:
            raise AuthenticationError('존재하지 않는 이메일입니다.')
        
        if not user.check_password(password):
            raise AuthenticationError('비밀번호가 다릅니다.')

class LogoutAPIView(APIView):
    def post(self,req):
        auth_logout(req)

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
    def post(self,req):

        regEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regEmail,req.data['email']):
            return JsonResponse({'Response' : '이메일 형식이 아닙니다.'})

        if req.data['password'] != req.data['confirm_password']:
            return JsonResponse({'Response' : '비밀번호와 확인 비밀번호가 일치하지 않습니다.'})
        else:
            hashed_password = make_password(req.data['password'])
            try:
                newUser = User(
                    email = req.data['email'],
                    password = hashed_password,
                    nickname = req.data['nickname']
                )
                newUser.save()
                user_info = {
                            'email':req.data['email'],
                            'user_id' : newUser.id,
                            'nickname' : req.data['nickname']
                }
                return Response({
                                'response': 'ok', 
                                'user_info' : user_info})
            except IntegrityError:
                return JsonResponse({'Response' : '이미 가입 된 이메일입니다.'})
