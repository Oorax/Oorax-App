from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import *
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .models import *

#from django.views.generic.base import TemplateView
#from registration.views import ResendActivationView,ActivationView,RegistrationView
urlpatterns = [

    url('obtain/', views.obtain, name='obtain'),
    url('edit-profile', views.edit_profile, name='edit_profile'),
    url('obtlogin/', views.obtlogin, name='obtlogin'),
    url(r'^lists',views.ListsView.as_view(), name="list"),
    url(r'^ajalog$',views.ajalog, name="ajalog"),
    url(r'^ajax$',views.ajax, name="ajax"),
    url(r'^zignup$',views.zignup, name="zignup"),
    url(r'index', views.index, name="index"),
    url(r'accueil', views.accueil, name="accueil"),
    url(r'home', views.home, name="home"),
    url(r'sexion-quiz', views.sexion_quiz, name="sexion_quiz"),
    url(r'^quiz/(?P<id>\d+)/chapitres$', views.mes_quiz, name='mes_quiz'),
    url(r'^choix-quiz$', views.choix_quiz, name='choix_quiz'),
    url(r'^check$', views.check, name='check'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'categorie', views.categorie, name="categorie"),
    url(r'mes-cours', views.mes_cours, name="mes_cours"),
    url(r'domaine', views.domaine, name="domaine"),
    url(r'^cour/(?P<id>\d+)/edite$', views.cour_edit, name='cour_edit'),
    url(r'^cour/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Cour, success_url="oorax/mes-cours"),
        name='cour_delete'),
    url(r'user-cour', views.user_mes_cours, name="user_mes_cours"),
    url(r'^cour-detail/(?P<id>\d+)$', views.cour_details, name='cour_details'),
    url(r'^detail-user/(?P<id>\d+)$', views.detail_user_cour, name='detail_user_cour'),
    url(r'^achat-cour/$',views.achat_cour, name='achat_cour'),
    url(r'^chapitre/(?P<id>\d+)/edite$', views.chapitre_edit, name='chapitre_edit'),
    url(r'^chapitre/(?P<pk>\d+)/delete$', DeleteView.as_view(model=Chapitre, success_url="oorax/cour"),
        name='chapitre_delete'),

    url(r'^achat/(?P<id>\d+)/lesson$', views.achat_lesson, name='achat_lesson'),
    url(r'^cour/(?P<id>\d+)/details$', views.contenu_mes_cours, name='contenu_mes_cours'),

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
    url(r'^__envoi_evaluation/',views.__envoi_evaluation,name='__envoi_evaluation'),
    url(r'^envoi_evaluation_chap/',views.envoi_evaluation_chap,name='envoi_evaluation_chap'),

    url(r'^administration/',views.administrer,name='administrer'),

    url(r'corrige', views.question_answer,name="question_answer"),
    url(r'inscription/(?P<id>\d+)', views.inscription, name="inscription"),
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
    url(r'liste-activation/(?P<id>\d+)/$', views.activation_liste,name="activation_liste"),
    url(r'block/(?P<id>\d+)/$', views.block_liste,name="block_liste"),
    url(r'white/(?P<id>\d+)/$', views.white_liste,name="white_liste"),

    url(r'abonnee/(?P<id>\d+)/$', views.detail_abonnees,name="detail_abonnees"),



    url(r'glisser/$', views.glisser,name='glisser'),

    url(r'option/(?P<id>\d+)/choise', views.option_page, name="option_page"),
    url(r'evaluation', views.evaluation, name="evaluation"),
    url(r'interrogation/(?P<id>\d+)/', views.interrogation, name="interrogation"),

    url(r'interro/(?P<id>\d+)/', views.faire_interro, name="faire_interro"),
    url(r'chapitre/(?P<id>\d+)/examen$', views.chap_evalua, name="chap_evalua"),

    url(r'cour', views.cour, name="cour"),
    url(r'statistique', views.stat_users, name="stat_users"),

    url(r'compte/$', views.compte_credit, name="compte_credit"),
    url(r'recharger/$', views.recharger_compte, name="recharger_compte"),
    url(r'transfert-credit/$', views.transfert_credit, name="transfert_credit"),
    url(r'historique/$', views.historique, name="historique"),

    url(r'login/$',auth_views.LoginView.as_view(template_name='registration/login.html'),name='auth_login'),
    url(r'register/$', views.signup, name='signup'),
    url(r'creer-code-secret/$', views.creer_code_secret, name='creer_code_secret'),
    url(r'actualisation/$', views.__actualisation__,name='__actualisation__'),
    url(r'choix_question/$', views.choix_question, name='choix_question'),


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