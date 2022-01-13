from rest_framework import serializers
from .models import Sneakers

class SneakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sneakers
        fields = '__all__'