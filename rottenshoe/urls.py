from django.urls import path
from . import views


app_name = 'rotten'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/',views.boardPost, name = 'boardPost'),
    path('detail/<int:id>',views.detail, name= 'detail'),
    path('login',views.login, name = 'login'),
    path('logout',views.logout, name = 'logout'),
    path('register',views.register, name = 'register'),
    path('detail/comment' , views.comment,name = 'comment'),
    path('mypage',views.myPage,name='mypage'),
    path('search/',views.search, name = 'search'),

] 
