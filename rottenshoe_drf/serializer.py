from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Sneakers,User

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

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 200)
    passowrd = serializers.CharField(max_length = 200, write_only = True)
    token = serializers.CharField(max_length = 255, read_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email = email)

        if user is None:
            return {'Response' : email + "로 가입한 이력이 없습니다."}
        
