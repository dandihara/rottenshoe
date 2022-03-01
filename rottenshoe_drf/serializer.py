from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rottenshoe.models import CopOrDrop
from .models import Sneakers,User,Comment


import datetime
#스니커즈 데이터 화면에 따른 분할
class SneakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneakers
        fields = '__all__'

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneakers
        fields = ['id','sneaker_name','brand','cop_percent','thumbnail']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self,instance,data):
        instance.comment = data.get('comment',instance.comment)
        instance.update_time = datetime.datetime.now()
        instance.save()
        
#jwt 변형 토큰 생성(login)
#토큰 내부 user_id, nickname만 저장
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['nickname'] = user.nickname
        return token

# 회원가입

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','nickname','password','confirm_password']
    # save 오버라이딩 -> 조건부 저장
    def save(self,data):
        if data['confirm_password'] == data['password']:
            User(email = data['email'],
                nickname = data['nickname'],
                password = data['password']).save()


class CoD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CopOrDrop
        fields = '__all__'


class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname','email','created_time']


    def update(self,instance,data):
        instance.nickname = data['nickname']
        instance.save()