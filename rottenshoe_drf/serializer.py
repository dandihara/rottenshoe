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
# pop으로 바로 들어갈 아이템만 남기고 처리.
class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    nickname = serializers.CharField()
    password = serializers.CharField(min_length = 8)

    class Meta:
        model = User
        fields = ('email','nickname','password')

    #pop은 말 그대로 pop. validated_data에서 가져오면서 그 부분은 제거됨.
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CoD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CopOrDrop
        fields = ['choice']