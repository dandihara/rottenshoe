
from django.urls import path,include,re_path
from . import views

app_name ='rottenshoe_drf'

urlpatterns = [
    path("",views.IndexAPIView.as_view(),name = 'main'),
    path("<str:category>",views.ListAPIView.as_view(),name = 'main-option'),
    path("detail/<int:id>",views.DetailAPIView.as_view()),
    path("cop/",views.CopOrDropAPIView.as_view()),
    path("register/",views.RegisterAPIView.as_view(), name = 'register'),
    path("comment/",views.CommentAPIView.as_view(),name = 'comment'),
    path("search/<str:keyword>",views.SearchAPIView.as_view(),name='search'),
]