from django.shortcuts import get_object_or_404
from rottenshoe_drf import serializer
from rottenshoe_drf.serializer import SneakerSerializer
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .token import *


'''
1)메인페이지
2)상세페이지
3)로그인, 로그아웃
4)댓글 작성

'''
        
class IndexAPIView(APIView):
    def get(self,req):
        newList = Sneakers.objects.all().order_by('-retail_date') # 출시일순 - 최신순
        hotList = Sneakers.objects.all().order_by('-cop_count') # 점수순
        newList = SneakerSerializer(newList, many = True)
        hotList = SneakerSerializer(hotList, many = True)

        data = {
            'newList' : newList,
            'hotList' : hotList
        }
        # 더보기 클릭 시 전체 리스트 전송(newList, hotList 따로 운용)
        return Response([newList.data[:5],hotList.data[:5]], 200)

class LoginAPIVIew(APIView):
    def post(self,req):
        pass

class LogoutAPIView(APIView):
    def post(self,req):
        pass
class CopOrDropAPIView(APIView):
    #cop or drop 평가 저장
    def post(self,req):
        s_id = req.data['id']
        board = get_object_or_404(Sneakers, id = s_id)
        board.total_count += 1

        if req.data['cop'] == 1:
            board.cop_count += 1

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
