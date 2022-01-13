from django.urls import path,re_path
from . import views


app_name = 'rotten'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('detail/<int:id>',views.detail, name= 'detail'),
    path('login',views.login, name = 'login'),
    path('logout',views.logout, name = 'logout'),
    path('register',views.register, name = 'register'),
    path('detail/comment' , views.comment,name = 'comment'),
    path('mypage',views.myPage,name='mypage'),
    path('search/<str:q>',views.search, name = 'search'),
    #re_path(r'^search(?P<q>.+)',views.search),
] 
