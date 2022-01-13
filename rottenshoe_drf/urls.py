from django.urls import path,re_path
from . import views

app_name ='rottenshoe_drf'

urlpatterns = [
    path('', views.index, name = 'index'),
    # path('detail/<int:id>',views.detail, name= 'detail'),
    # path('register',views.register, name = 'register'),
    # path('detail/comment' , views.comment,name = 'comment'),
    # path('mypage',views.myPage,name='mypage'),
    # path('search/<str:q>',views.search, name = 'search'),
]