"""Formations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from oorax import views
#from reservation import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
   # url('api/v1/', include('api.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^oorax/', include('oorax.urls')),
    url(r'reservation/', include('reservation.urls')),
    url(r'^', include('searchs.urls')),
    url(r'^getdetails/', views.getdetails, name="getdetails"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^activate/', include('registration.backends.default.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
