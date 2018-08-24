from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from oorax.models import *

urlpatterns = [

    url(r'index', views.index, name="index"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)