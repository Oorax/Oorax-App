from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from .models import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import *
#from django.views.generic.base import TemplateView
#from registration.views import ResendActivationView,ActivationView,RegistrationView

urlpatterns = [

    url(r'index', views.index, name="index"),
    url(r'home', views.home, name="home"),
    url(r'categorie', views.categorie, name="categorie"),

    url(r'^cour/(?P<id>\d+)/edite$', views.cour_edit, name='cour_edit'),
    url(r'^cour/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Cour, success_url="oorax/cour"),
        name='cour_delete'),

    url(r'^chapitre/(?P<id>\d+)/edite$', views.chapitre_edit, name='chapitre_edit'),
    url(r'^chapitre/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Chapitre, success_url="oorax/cour"),
        name='chapitre_delete'),

    url(r'^lesson/(?P<id>\d+)/edite$', views.lesson_edit, name='lesson_edit'),
    url(r'^lesson/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Lesson, success_url="oorax/cour/"),
        name='lesson_delete'),

    url(r'^details/(?P<id>\d+)/statistique$', views.details, name='details'),
    #url(r'^lesson/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Lesson, success_url="oorax/cour"),
        #name='lesson_delete'),

    url(r'^contenue/(?P<id>\d+)/edite$', views.contenu_edit, name='contenu_edit'),
    url(r'^contenue/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Chapitre, success_url="oorax/cour"),
        name='contenu_delete'),
    url(r'^envoi_evaluation/',views.envoi_evaluation,name='envoi_evaluation'),
    url(r'corrige', views.question_answer,name="question_answer"),
    url(r'inscription/(?P<id>\d+)/cour', views.inscription, name="inscription"),
    url(r'creer/(?P<id>\d+)/question', views.question, name="question"),
    url(r'^getdetails/', views.getdetails, name="getdetails"),
    url(r'^cherchap/', views.cherchap, name="cherchap"),
    url(r'^cherless/', views.cherless, name="cherless"),
    url(r'achat', views.achat, name="achat"),
    url(r'cour/(?P<id>\d+)/chapitre', views.chapitre_cour, name="chapitre_cour"),
    url(r'cour/chapitre/lesson', views.lesson_chapitre, name="lesson_chapitre"),
    url(r'cour/lesson/(?P<id>\d+)/contenu', views.contenu_lesson, name="contenu_lesson"),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    url(r'glisser/$', views.glisser,name='glisser'),

    url(r'option/(?P<id>\d+)/choise', views.option_page, name="option_page"),
    url(r'evaluation', views.evaluation, name="evaluation"),
    url(r'interrogation/(?P<id>\d+)/', views.interrogation, name="interrogation"),

    url(r'interro/(?P<id>\d+)/', views.faire_interro, name="faire_interro"),

    url(r'cour', views.cour, name="cour"),
    url(r'statistique', views.stat_users, name="stat_users"),

    url(r'compte/$', views.compte_credit, name="compte_credit"),
    url(r'recharger/$', views.recharger_compte, name="recharger_compte"),
    url(r'transfert-credit/$', views.transfert_credit, name="transfert_credit"),
    url(r'historique/$', views.historique, name="historique"),

    url(r'login/$',auth_views.LoginView.as_view(template_name='registration/login.html'),name='auth_login'),
    url(r'register/$', views.signup, name='signup'),

    url(r'^login/$',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'),
        name='auth_login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(
            template_name='registration/logout.html'),
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy('auth_password_change_done')),
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('auth_password_reset_done')),
        name='auth_password_reset'),
    url(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='auth_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth_password_reset_complete')),
        name='auth_password_reset_confirm'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)