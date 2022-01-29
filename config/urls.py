"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from rottenshoe_drf.views import *
#jwt
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
#swagger
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi

schema_url_patterns = [ 
    path('api/', include('rottenshoe_drf.urls')), 
    ] 
schema_view_v1 = get_schema_view( 
    openapi.Info( title="rottenshoe_api", #타이틀
                    default_version='v1',
                    description="roteenshoe API 명세서",#설명 
                    terms_of_service="https://www.google.com/policies/terms/", 
                ),
                    public=True, 
                    permission_classes=(AllowAny,), 
                    patterns=schema_url_patterns,
                    validators= ['flex'],
                )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('rottenshoe.urls')),
    path('api/',include('rottenshoe_drf.urls')),
    path('token/obtain/',ObtainTokenPairWithNickname.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    #swagger
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'), 
    path('swagger', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
