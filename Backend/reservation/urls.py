from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'matiere', views.matiere, name="matiere"),
    url(r'session', views.session, name="session"),
    url(r'reservation',views.reservation, name="reservation"),
    url(r'user', views.user_eleve, name="user_eleve"),
    url(r'^payer/(?P<id>\d+)/reserve', views.envoi_reserve, name='envoi_reserve'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)