from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
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

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

