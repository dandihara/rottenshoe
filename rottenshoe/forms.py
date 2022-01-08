from django import forms

from .models import Sneakers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class BoardForm(forms.ModelForm):
    class Meta:
        model = Sneakers
        fields = ['thumbnail','sneaker_name','model_number','brand','price','retail_date']
        widgets = {
            'retail_date' : forms.DateInput(format= ("%Y/%m/%d"), attrs={'class':'form-control','placeholder':'출시일자','type':'date'}),

        }
        labels = {
            'thumbnail' : '메인 이미지',
            'sneaker_name' : '모델명',
            'model_number':  '모델번호',
            'brand' : '브랜드',
            'price' : '가격',
            'retail_date' : '출시일'
        }


class UserForm(UserCreationForm):
    nickname = forms.CharField(label = '닉네임')
    class Meta:
        model = User
        fields = ['username', 'password1' , 'password2','nickname']

