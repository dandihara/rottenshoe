from pyexpat import model
from rest_framework import serializers
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