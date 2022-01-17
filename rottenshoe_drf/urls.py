
from django.urls import path,include,re_path
from . import views

#drf router
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'index',views.IndexViewSet,basename='index')
app_name ='rottenshoe_drf'

urlpatterns = [
    path("",views.IndexAPIView.as_view(),name = 'main'),
    path("<str:mode>",views.ListAPIView.as_view(),name = 'main-option'),
    path("detail/<int:id>",views.DetailAPIView.as_view()),
    path("login/",views.LoginAPIVIew.as_view()),
    path("logout/",views.LogoutAPIView.as_view()),
    path("cop/",views.CopOrDropAPIView.as_view()),
    path("register/",views.RegisterAPIView.as_view(), name = 'register'),
]