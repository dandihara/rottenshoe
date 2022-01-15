
from django.urls import path,include
from . import views

#drf router
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'index',views.IndexViewSet,basename='index')
app_name ='rottenshoe_drf'

urlpatterns = [
    path("",views.IndexAPIView.as_view()),
    path("detail/<int:id>",views.DetailAPIView.as_view()),
    path("login",views.LoginAPIVIew.as_view()),

]