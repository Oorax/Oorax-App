import json as simplejson
import collections
from itertools import count

from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import transaction
from pyquery import PyQuery as pq
import postmarkup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import bbcode
import time
from html.parser import HTMLParser
from precise_bbcode.bbcode import get_parser
from django.contrib.auth.views import logout
from django.http import HttpResponse, QueryDict
import MySQLdb as db
import random

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from oorax.serializers import UserSerializer
from .forms import *
from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from django.db.models import Q
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
#from django.contrib.auth import views as auth_views
#from django.utils import text
import requests
from rest_framework import viewsets
#from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated
# Django rest ap
def detail_abonnees(request,id):
    users=request.user.id
    cours=Inscrit.objects.filter(cour_id=id)
    custom=CustomUser.objects.all()

    return render(request, 'auteurs/auteurs.html',{'cours':cours,'custom':custom})




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

def obtain(request):
    a=request.user
    if a:
        response = requests.get('http://127.0.0.1:8000/users/?format=json')
        geodata = response.json()
        list=[]
        for x in geodata['results']:
            list.append(x["username"])
        return render(request, 'ajax/liste.html', {
            'list': list,
            #'country': geodata['email']
        })
    else:
        return HttpResponse('pas authentifiaé')


def obtlogin(request):
    response = requests.get('http://127.0.0.1:8000/rest-auth/login/')
    print('la reponse ',response)



#class HelloView(APIView):
#    def get(self,requests):
 #       return HttpResponse('ok')
    #permission_classes = (IsAuthenticated,)
    #def get(self,request):
     #   content={'message':'Helle word'}
      #  return Response(content)

#ajax
def ajax(request):
    return render (request,'ajax/ajax.html')
def zignup(request):
    return render(request,'ajax/signup.html')
def ajalog(request):
    return render(request, 'ajax/index.html')


#liste users

class ListsView(ListAPIView):
    queryset = CustomUser.objects.all()
   # obj = CustomUser.objects.first()
    serializer_class = UserSerializer
   # obj_data = UserSerializer(obj)
    #print('resultat',obj_data.data)


#page d'accueil



def index(request):
    users=request.user.id

    print(users)


    if users:
        checked=Check.objects.filter(id=1)
        fonc = CustomUser.objects.get(id=users)
        cust=CustomUser.objects.all()
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email=fonc.email
            if fonc.image:
                img=fonc.image.url
            else:
                img="pas d'image"

            inscrit=Inscrit.objects.all()
            cour_vendu=[]
            cour_publies=[]
            cour_inscrit=[]
            g=[]
            tab2D={}

            var1 = Transaction.objects.filter(user_sortie_id=users)
            var2 = Transaction.objects.filter(user_entree_id=users)
            x = 0
            y = 0
            for trans in var1:
                x = x + trans.montant
            for tran in var2:
                y = y + tran.montant + tran.bonus
            soldes = int(y - x)
            solde='{:,}'.format(soldes)
            #solde=float(soldesString.replace(',', '.'))
            print('mon solde est', solde)


            for x in inscrit:
                var=Cour.objects.filter(Q(id=x.cour_id) & Q(auteur_id=users))
                for y in var:
                    cour_vendu.append(y.id)
            h=len(cour_vendu)
            print(h)
            cours=Cour.objects.filter(auteur_id=users)

            for z in cours:
                cour_publies.append(z.id)
            c=len(cour_publies)
            print('cour publie',cour_publies)

            page = request.GET.get('page', 1)
            paginator = Paginator(cour_publies, 10)
            try:
                cou = paginator.page(page)
            except PageNotAnInteger:
                cou = paginator.page(1)
            except EmptyPage:
                cou = paginator.page(paginator.num_pages)
            print(cou)
            for m in cou:
                for t in inscrit:
                    if m is t.cour_id:
                        g.append(t.cour_id)
                tab2D[m]= g.count(m)
                #tab2D[0].append(m)
                #tab2D[1].append(g.count(m))
                #a=len(tab2D[1])

            print('nommr',tab2D)




            ins=Inscrit.objects.filter(custom_id=users)
            for i in ins:
                cour_inscrit.append(i.cour_id)
            d=len(cour_inscrit)
            form = TransferForm()
            form3 = RechargerForm()
            form2 = Recharger2Form()
            omoney = Mobilemoney.objects.all()
            return render(request, 'auteurs/auteurs.html', {'cust':cust,'g':g,'inscrit':inscrit,'cours':cours,'form':form,
                                                            'checked': checked,'h':h,'solde':solde,'form2':form2,
                                                            'form3':form3,'omoney':omoney,'cou':cou,
                                                            'c':c,'d':d,'email':email,'img':img,'tab2D':tab2D })

        elif fonc.fonction == 'Apprenants' and fonc.email_validated == 1:
            b=0
            email=fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
            return render(request, 'registration/index.html', {'checked': checked, 'b': b, 'email':email,'img':img})

        else:
            return HttpResponse('en attente de validation')

    else:
        checked=Check.objects.filter(id=1)
        return render(request, 'registration/index2.html', {'checked': checked, })

def administrer(request):
    use=request.user.id
    print(use)

    if use:

        fonc = CustomUser.objects.get(id=use)
        if fonc.is_superuser:
            users = CustomUser.objects.all()
            return render(request, 'registration/administration.html', {'users': users})


        else:
            return HttpResponse('vous n\'êtes pas l\'admin')

    else:
        return redirect('index')

def accueil(request):
    users=request.user.id
    return render(request,'registration/accueil.html',{'users':users})

def home(request):
    cours = Cour.objects.filter(etat_cour=0)
    categories = Categorie.objects.all()
    return render(request,'registration/home.html',{'cours':cours,'categories':categories})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            us=user.id
            cust = CustomUser.objects.get(id=us)

            s=str(us)
            cust.code_afiliation = 'date 2018'+ s

            cust.save()
            form2 = RechargerForm()
            trans = form2.save(commit=False)
            custom = CustomUser.objects.all()
            #for c in custom:
               # print('parrain',cust.parrain)
              #  if cust.parrain:
                   # if c.code_afiliation == cust.parrain:
                        #trans.user_entree_id = us
                        #trans.libelle = 'bonus inscription'
                        #trans.bonus = 200
                        #trans.save()
                        #custt=CustomUser.objects.get(code_afiliation=cust.parrain)
                        #print('parr',custt.id)
                        #form3 = RechargerForm()
                        #tran = form3.save(commit=False)
                        #tran.user_entree_id = custt.id
                        #trans.libelle = 'bonus inscription'
                        #tran.bonus = 201
                       # tran.save()
                        #current_site = get_current_site(request)
                        #subject = 'Activate Your MySite Account'
                        #message = render_to_string('registration/activation_email.html', {
                          #  'user': user,
                           # 'domain': current_site.domain,
                           # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                            #'token': account_activation_token.make_token(user),
                        #})
                       # user.email_user(subject, message)
                        #return render(request, 'registration/login.html')
                    #else:
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)
            return redirect('/oorax/login/')

        else:
            redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})

#edite profile
@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return redirect('/oorax/profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'auteurs/modier_profile.html', {
        'user_form': user_form,

    })
# vue de la page activation de compte
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
       # user.is_active = True
        user.email_validated = True
        user.save()
        logout(request)
        return redirect('/oorax/login/')
    else:
        return render(request, 'registration/activate.html')

#vue de la page message activation de compte
def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

#page enregistrement categorie
def categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            parent = request.POST["hide"]
            if parent:
                user.parent = parent
                user.save()
            else:
                user.save()
            return redirect('categorie')
    else:
        a=[]
        form = CategorieForm()
        categories = Categorie.objects.filter(parent__isnull=True)
        categorie = Categorie.objects.filter(parent__isnull=False)
        for cat in categorie:
            a.append(cat.parent)

    return render(request, 'registration/categorie_form.html', {'a':a,'categorie':categorie,'form': form, 'categories':categories})

#enregistrement cour
def cour(request):

    if request.method == 'POST':
        form = CourForm(request.POST,request.FILES)
        if form.is_valid():
            nom_cat = request.POST["hides"]
            nom_dom = request.POST["hides2"]

            cat = Categorie.objects.get(nom_categorie=nom_cat)
            dom = Domaine.objects.get(nom_domaine=nom_dom)
            print(cat.id)
            user = form.save(commit=False)
            user.categorieid_id = cat.id
            user.domaineid_id=dom.id
            user.etat_cour=0

            user.save()
        categories = Categorie.objects.all()
        domaine = Domaine.objects.all()
        cours = Cour.objects.filter(etat_cour=0)
        return render(request, 'registration/cour_register_form.html',
                          {'form': form, 'categories': categories,'domaine':domaine, 'cours': cours})

    else:
        form = CourForm(request.POST, request.FILES)
        categories = Categorie.objects.all()
        domaine = Domaine.objects.all()
        cours = Cour.objects.filter(etat_cour=0)
    return render(request, 'registration/cour_register_form.html',{'form': form,'domaine':domaine,'categories':categories,'cours':cours})

#modiffier cour
def cour_edit(request,id):
    cour = get_object_or_404(Cour, id=id)
    form = CourForm(request.POST or None, instance=cour, )

    if form.is_valid():
        cat_name = request.POST["hides"]
        cat = Categorie.objects.get(nom_categorie=cat_name)
        user = form.save(commit=False)
        user.categorieid_id = cat.id
        print(user.categorieid_id)
        user.etat_cour = 0
        user.save()
        return redirect('cour')
    categories = Categorie.objects.all()

    cours = Cour.objects.filter(etat_cour=0)
    return render(request, "registration/cour_register_form.html",
                  {'form': form,'categories':categories,'cours':cours,})

#supprimer cour
def cour_delete(request,id):
    cour = Cour.objects.get(id=id)
    cour.delete()
    return redirect('mes_cours')

#Ajouter chapitre
def chapitre_cour(request,id):
    cour = Cour.objects.get(id=id)
    users=request.user.id
    a=cour.id
    nom=cour.titre
    #form = ChapitreForm(request.POST or None, instance=Cour, )
    if request.method == 'POST':
        form = ChapitreForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.courid_id = a
            user.save()
            print(user.courid_id)
            return redirect('chapitre_cour',id=cour.id)

    else:
        form = ChapitreForm()
        formless = LessonForm()
        chap_liste=[]
        lesson = Lesson.objects.all()
        chapitre = Chapitre.objects.filter(courid_id=a)
        for pp in chapitre:
            chap_liste.append(pp.id)
        print(chap_liste)
        fonc = CustomUser.objects.get(id=users)
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
        return render(request, "auteurs/chapitre_cour.html",
                      {'formless': formless,
                       'email':email,
                       'img':img,
                       'form': form,
                       'lesson':lesson,
                       'nom':nom,'a':a,
                       'chap_liste':chap_liste,
                       'chapitre':chapitre})

#modiffier chapitre
def chapitre_edit(request,id):
    cour = get_object_or_404(Chapitre, id=id)
    cours = Cour.objects.all()
    for c in cours:
        if cour.courid_id is c.id:
            a=cour.courid_id
            nom=c.titre

    form = ChapitreForm(request.POST or None, instance=cour, )
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('chapitre_edit', id=cour.id)
    else:
        chapitre = Chapitre.objects.filter(courid_id=a)
        return render(request, "registration/chapitre_cour.html",
                      {'form': form,'nom':nom,'chapitre':chapitre,})

#supprimer chapitre
def chapitre_delete(request,id):
    chapitre = Chapitre.objects.get(id=id)
    chapitre.delete()
    return redirect('chapitre_delete', pk=cour.pk)

#Ajouter lesson
def lesson_chapitre(request):
    id_chap = int(request.POST["less"])
    print(id_chap)
    chapitre = Chapitre.objects.get(id=id_chap)
    a=chapitre.id
    b=chapitre.courid_id

    liste_evalu=[]
    evaluation=Evaluation.objects.all()
    for eva in evaluation:
        liste_evalu.append(eva.id)
    #print(liste_evalu)
    m=chapitre.courid_id
    nom = chapitre.nom_chapitre
    #form = ChapitreForm(request.POST or None, instance=Cour, )
    if request.method == 'POST':
        formless = LessonForm(request.POST)
        if formless.is_valid():
            user = formless.save(commit=False)
            user.chapitreid_id = a
            user.save()
            #print(user.chapitreid_id)
            return redirect('chapitre_cour',id=b)

    else:

        lesson = Lesson.objects.filter(chapitreid_id=a)
        evaluation = Evaluation.objects.exclude(typeId='')
        optEva = Option.objects.all()
        chapitres = Chapitre.objects.filter(courid_id=b)
        list=[]
        quesevalu = QuestionEvaluation.objects.all()
        for x in quesevalu:
            if x.evaluation_id in list:
                pass
            else:
                list.append(x.evaluation_id)

        questionoption = OptionQuestion.objects.all()
        question = Question.objects.all()
        listEva=[]
        li=[]
        for evalu in evaluation:
            listEva.append(evalu.typeId)

            for l in evalu.typeId:
                li.append(l)
        print(len(li))
        print(len(listEva))
        cour = Cour.objects.all()
        for cou in cour:
            if cou.id == m:
                j=cou.titre
        return render(request, "registration/chapitre_cour.html",
                      {'liste_evalu':liste_evalu,
                        'a':a,
                       'chapitres':chapitres,
                       'list':list,
                       'optEva':optEva,

                       'cour':cour,
                       'j':j,
                       'm':m,
                       'nom':nom,
                       'quesevalu': quesevalu,
                       'questionoption': questionoption,
                       'question': question,
                       'lesson':lesson})

#modiffier lesson
def lesson_edit(request,id):
    lesson = get_object_or_404(Lesson, id=id)
    form = LessonForm(request.POST or None, instance=lesson, )
    chapitre=Chapitre.objects.all()
    for ch in chapitre:
        if lesson.chapitreid_id is ch.id:
            a=ch.id
            m=ch.courid_id
            nom = ch.nom_chapitre
    cour = Cour.objects.all()
    for cou in cour:
        if cou.id == m:
            j = cou.titre

    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('lesson_edit',id=lesson.id)
    else:
        lesson = Lesson.objects.filter(chapitreid_id=a)
        return render(request, "registration/lesson_chapitre.html",
                      {'form': form,'lesson':lesson,'j':j,'a':a,'nom':nom,'m':m})

#supprimer lesson
def lesson_delete(request,id):
    lesson = Lesson.objects.get(id=id)
    lesson.delete()
    return redirect('cour')

#ajouter contenu lesson
def contenu_lesson(request,id):
    lesson = Lesson.objects.get(id=id)
    users=request.user.id
    a = lesson.id
    m = lesson.chapitreid_id
    nom=lesson.nom_lesson
    chapitre = Chapitre.objects.all()
    for f in chapitre:
        if f.id == m:
            g=f.courid_id
            print(g)

    # form = ChapitreForm(request.POST or None, instance=Cour, )
    if request.method == 'POST':
        form = ContenuForm(request.POST)
        form2 = ContenuLienForm(request.POST)
        choix1=request.POST["hide"]

        if choix1:

            if form2.is_valid() or form.is_valid():
                if request.POST["hide"]=='Lien':
                    users = form2.save(commit=False)
                    users.lessoneid_id = a
                    users.types = request.POST["hide"]
                    users.save()
                    return redirect('contenu_lesson', id=lesson.id)
                else:
                    user = form.save(commit=False)
                    user.lessoneid_id = a
                    #user.types = request.POST["hides"]
                    user.save()
                    return redirect('contenu_lesson', id=lesson.id)
        else:
            return HttpResponse('non')


    else:
        form = ContenuForm()
        form2 = ContenuLienForm()
        contenu = Contenue.objects.filter(lessoneid_id=a)
        #parser = get_parser()
        print(postmarkup.parser.PostMarkup)
        #parser = bbcode.Parser()
        markup =postmarkup.parser.PostMarkup()
        #bbcode = "[b]Hello, World![/b]"


        cour = Cour.objects.all()
        for cous in cour:
            if cous.id == g:
                cou=cous.titre
                fo=cous.id
                #print(cou)

        chapitre = Chapitre.objects.all()
        for cha in chapitre:
            if cha.id == m:
                c=cha.nom_chapitre
                p=cha.id
                #print(c)
                #print(p)

        fonc = CustomUser.objects.get(id=users)
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
        return render(request, "auteurs/contenu_cour.html",
                      {'form': form,'img':img,'email':email,
                       'form2':form2,
                       'cour':cour,
                       'fo':fo,
                       'cou':cou,
                        'm':m,
                       'p':p,
                       'c':c,
                       'nom':nom,
                       'chapitre':chapitre,
                       'contenu': contenu,
                       
                       }
                      )

#modiffier contenu
def contenu_edit(request,id):
    contenu = get_object_or_404(Contenue, id=id)
    form = ContenuForm(request.POST or None, instance=contenu, )
    chapitre = Chapitre.objects.all()
    lesson = Lesson.objects.all()
    for less in lesson:
        if contenu.lessoneid_id is less.id:
            m=less.chapitreid_id
            nom=less.nom_lesson
            a=less.id
    for f in chapitre:
        if f.id == m:
            g = f.courid_id
            c = f.nom_chapitre
            p = f.id

    cour = Cour.objects.all()
    for cous in cour:
        if cous.id == g:
            cou = cous.titre
            fo = cous.id

    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('contenu_edit',id=contenu.id)
    else:
        contenu = Contenue.objects.filter(lessoneid_id=a)
        return render(request, "registration/contenu_cour.html",
                      {'form': form,'contenu':contenu,'fo':fo,
                       'cou':cou,
                        'm':m,
                        'nom':nom,
                       'p': p,
                       'c': c,
                       })

#supprimer contenu
def contenu_delete(request,id):
    contenu = Contenue.objects.get(id=id)
    contenu.delete()
    return redirect('cour')

#page compte crédit
def compte_credit(request):
    users=request.user
    custom=CustomUser.objects.get(id=users.id)
    print(custom.code_secret)
    if custom.code_secret:
        return render(request, 'registration/compte_credit.html')
    else:
        return redirect('creer_code_secret')

def creer_code_secret(request):
    if request.method == 'POST':
        users = request.user
        codes=request.POST["code"]
        print(codes)
        custom = CustomUser.objects.get(id=users.id)

        custom.code_secret=codes
        custom.save()
        return redirect('compte_credit')
    else:
        return render(request, 'registration/creer_code_secret.html')

#page charger compte
def recharger_compte(request):
    if request.method == 'POST':
        form2 = RechargerForm(request.POST)
        form3 = Recharger2Form(request.POST)
        choix1=request.user
        print(choix1.identifiant)
        if form2.is_valid() :
            x=request.POST["ref"]
            print(x)
            if x==choix1.identifiant:
                users = form2.save(commit=False)
                users.mobile_moneyId_id =request.POST["hide"]
                users.reference = x
                users.user_entree_id = choix1.id
                users.bonus = 300
                users.montant = 5000
                users.libelle = 'Rechargement'
                users.save()
                fonc = CustomUser.objects.get(id=choix1.id)
                if fonc.fonction == 'Auteurs':
                    email = fonc.email
                    if fonc.image:
                        img = fonc.image.url
                    else:
                        img = "pas d'image"
                    print(img)
                    form2 = RechargerForm()
                    form3 = Recharger2Form()
                    omoney = Mobilemoney.objects.all()
                    montemps = time.time()
                    return render(request, 'auteurs/auteurs.html', {'montemps': montemps, 'omoney': omoney,
                                                                             'form2': form2, 'form3': form3,
                                                                             'email': email, 'img': img})

            else:
                print('echeque')
                return redirect('index')
        else:
            print('echeque')
            choix1 = request.user
            fonc = CustomUser.objects.get(id=choix1.id)
            if fonc.fonction == 'Auteurs':
                email = fonc.email
                if fonc.image:
                    img = fonc.image.url
                else:
                    img = "pas d'image"
                form2 = RechargerForm()
                form3 = Recharger2Form()
                omoney = Mobilemoney.objects.all()
                montemps = time.time()
                return render(request, 'auteurs/recharger_compte.html',{'montemps':montemps,'omoney':omoney,
                                                                        'form2':form2,'form3':form3,'email':email,'img':img})

            else:
                form2 = RechargerForm()
                form3 = Recharger2Form()
                omoney = Mobilemoney.objects.all()
                montemps = time.time()
                return render(request, 'registration/recharger_compte.html',
                              {'montemps': montemps, 'omoney': omoney, 'form2': form2, 'form3': form3})


#page d'actualisation
def __actualisation__(request):

    #creer fichier json et acualiser
    objects_list = []
    actu = ServeurOrange.objects.all()
    for row in actu:
        d = collections.OrderedDict()
        d['id'] = row.id
        d['Reference'] = row.reference
        d['Montant'] = row.montant
        d['Numero'] = row.num_transfert

        objects_list.append(d)
    j = simplejson.dumps(objects_list)
    with open("orangeMoney.js", "w") as f_write:
        simplejson.dump(objects_list, f_write)


    #lire fichier json
    tran = Transaction.objects.all()
    with open('orangeMoney.js') as json_data:
        data = simplejson.load(json_data)
    list_tra=[]
    list_mont=[]
    for tra in tran:
        for ac in data:
            if tra.reference == ac["Reference"]:
                if tra.montant == ac["Montant"]:
                    list_tra.append(ac["Reference"])
                else:
                    users = Transaction.objects.get(reference=ac["Reference"])
                    users.montant=ac['Montant']
                    users.libelle='chargement'
                    users.save()
    return render(request,'registration/actualisation.html')

#page transfert credi
def transfert_credit(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        users=request.user.id
          # retrouver le recepteur
        var1 = Transaction.objects.filter(user_sortie_id=users)
        var2 = Transaction.objects.filter(user_entree_id=users)
        print('coocl')

        x = 0
        y = 0
        for trans in var1:
            x = x + trans.montant
        for tran in var2:
            y = y + tran.montant + tran.bonus
        soldes = int(y - x)
        solde = '{:,}'.format(soldes)

        if form.is_valid():
            a = request.POST["ident"]#recuperer identifiant du recepteur
            lui = CustomUser.objects.filter(identifiant=a)
            print('coocl')

            m= request.POST["montant"]
            montant = m
            for s in lui:
                print(s.identifiant)
            moi = request.user
            if s.identifiant and soldes > int(montant):
                users = form.save(commit=False)
                users.user_sortie_id = moi.id
                users.user_entree_id = s.id
                users.reference = s.identifiant
                users.libelle = 'Transfert'
                users.save()
                fonc = CustomUser.objects.get(id=users)
                if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
                    b = 1
                    email = fonc.email
                    if fonc.image:
                        img = fonc.image.url
                    else:
                        img = "pas d'image"
                    print("auteur")
                    form = TransferForm()
                    form3 = RechargerForm()
                    form2 = Recharger2Form()
                    omoney = Mobilemoney.objects.all()
                    print('coocl')
                    return render(request, 'auteurs/historique.html', {'omoney':omoney,'email':email,'solde':solde,'img':img,'form': form,'form2':form2,'form3':form3})
                else:
                    form = TransferForm()
                    form3 = RechargerForm()
                    form2 = Recharger2Form()
                    omoney = Mobilemoney.objects.all()
                    # user = CustomUser.objects.all()
                    return render(request, 'registration/transfert_credit.html', {'omoney':omoney,'form': form,'form2':form2,'form3':form3})
            return redirect('/transfert_credit/')

    else:
        print('coocl')

        users=request.user.id
        fonc = CustomUser.objects.get(id=users)
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
                print("auteur")
                form = TransferForm()
                #user = CustomUser.objects.all()
            # return render(request, 'auteurs/historique.html',{'form':form})
        else:
            print('coocl')
            form = TransferForm()
            form = TransferForm()
            form3 = RechargerForm()
            form2 = Recharger2Form()

            omoney = Mobilemoney.objects.all()

            # user = CustomUser.objects.all()
            return render(request, 'registration/transfert_credit.html', {'omoney':omoney,'form': form,'form2':form2,'form3':form3})


#page inscription
def inscription(request,id):
    cour = Cour.objects.get(id=id)
    user=request.user
    id = cour.id
    titre = cour.titre
    prix = cour.prix
    customUser=CustomUser.objects.all()
    for cus in customUser:
        if cus.id is user.id:
            return render(request, "registration/inscription_cour.html", {'titre': titre, 'prix': prix, 'id': id})
        else:
            return redirect('signup')

def achat_lesson(request,id):
    less = Lesson.objects.get(id=id)
    user = request.user
    id = less.id
    titre = less.nom_lesson
    prix = 100
    customUser = CustomUser.objects.all()
    return render(request, "registration/achat_lesson.html", {'titre': titre, 'prix': prix, 'id': id})

def achat_cour(request):
    if request.method == 'POST':

        users = request.POST["users"]  # recuperer l'id du user
        courid = request.POST["courid"]  # recuperer l'id du cour
        form = InscritForm()
        insc = form.save(commit=False)
        insc.cour_id = courid
        insc.custom_id = users
        insc.save()
        return redirect('user_mes_cours')

def achat(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        users=request.POST["users"]#recuperer l'id du user
        lessid=request.POST["lessid"]#recuperer l'id du cour
        z = Lesson.objects.get(id=lessid)#retrouver l'id du cour
        var1 = Transaction.objects.filter(user_sortie_id=users)
        var2 = Transaction.objects.filter(user_entree_id=users)
        x = 0
        y = 0
        for trans in var1:
            x = x + trans.montant
            print('sortant',x)
        for tran in var2:
            y = y + tran.montant
            print('entrant', y)

        solde = int(y - x)
        print('result',solde)


        if solde >= 100:
            usertrans=form.save(commit=False)
            usertrans.user_sortie_id = users
            usertrans.montant = 100
            usertrans.libelle = 'Achat'
            usertrans.save()

            var3 = usertrans.id
            form2 = InscriptionForm()
            insc = form2.save(commit=False)
            insc.cour_id = lessid
            insc.transaction_id = var3
            insc.users_id= users
            insc.save()
            ch = Chapitre.objects.get(id=z.chapitreid_id)
            return redirect('detail_user_cour',id=ch.courid_id )
        else:
            return HttpResponse('sold insuffisant !!!')

    form = TransferForm()
    return render(request, "registration/home.html",{'form':form})

#page historique
def historique(request):
    user1 = request.user
    fonc = CustomUser.objects.get(id=user1.id)
    var1 = Transaction.objects.filter(user_sortie_id=user1.id)
    var2 = Transaction.objects.filter(user_entree_id=user1.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(var2, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    x = 0
    y = 0
    for trans in var1:
        x = x + trans.montant
    for tran in var2:
        y = y + tran.montant + tran.bonus
    soldes = int(y - x)
    solde = '{:,}'.format(soldes)
    # solde=float(soldesString.replace(',', '.'))
    print('mon solde est', solde)

    if fonc.fonction == 'Auteurs':
        email = fonc.email
        if fonc.image:
            img = fonc.image.url
        else:
            img = "pas d'image"
        form = TransferForm()

        form3 = RechargerForm()
        form2 = Recharger2Form()
        omoney = Mobilemoney.objects.all()
        montemps = time.time()
        var2 = Transaction.objects.filter(Q(user_entree_id=user1.id) | Q(user_sortie_id=user1.id))#recuperer les entrées=user.id OU sortie=user.id
        return render(request, 'auteurs/historique.html',{'users':users,'form3':form3,'omoney':omoney,'form': form,'form2':form2,
                                                          'solde':solde,'var2':var2,'email':email,'img':img})
    else:
        var2 = Transaction.objects.filter(
            Q(user_entree_id=user1.id) | Q(user_sortie_id=user1.id))  # recuperer les entrées=user.id OU sortie=user.id
        return render(request, 'registration/historique.html', {'solde':solde,'var2': var2})

#page creer qustion
def question(request,id):
    if request.method == 'POST':
        form=QuestionForm(request.POST)
        users = request.user.id
        lesson = request.POST["lessonid"]
        idlesson=Lesson.objects.all()
        for le in idlesson:
            if le.nom_lesson==lesson:
                p=le.id
        type = request.POST["typeid"]
        if form.is_valid():
            user = form.save(commit=False)
            user.lesson_id=p
            user.typequestion_id=type
            user.user_id=users
            user.save()
            quest_id=user.id
            essai = request.POST["essai"]
            q = QueryDict(essai, mutable=True)
            my = q.pop("b")
            conn = db.connect(host="localhost", user="root", password="", database="formation")
            cur = conn.cursor()
            cur2 = conn.cursor()
            for option in my:
                try:
                    cur.execute("INSERT INTO oorax_option (libelle)  VALUES (%s) ",[option])
                    a=cur.lastrowid
                    cur2.execute("INSERT INTO oorax_optionquestion (option_id,question_id)  VALUES (%s,%s) ", [a,quest_id])
                    conn.commit()
                except:
                    # Rollback in case there is any error
                    conn.rollback()
            question = Cour.objects.get(id=id)
            questions=question.id
            chap_liste = Chapitre.objects.filter(courid_id=question.id)
            type_question = TypeQuestion.objects.all()
            option = Option.objects.all()
            niveaus=Niveau.objects.all()
            fonc = CustomUser.objects.get(id=users)
            if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
                b = 1
                email = fonc.email
                if fonc.image:
                    img = fonc.image.url
                else:
                    img = "pas d'image"
                    print("auteur")
            return render(request, 'auteurs/question.html',
                          {'niveaus':niveaus,'option':option,'email':email,'img':img,
                           'chap_liste': chap_liste, 'type_question': type_question, 'form': form, 'questions':questions})
    else:
        users = request.user.id
        form = QuestionForm()
        form2 = OptionForm()
        question = Cour.objects.get(id=id)
        questions = question.id
        chap_liste = Chapitre.objects.filter(courid_id=question.id)
        type_question = TypeQuestion.objects.all()
        option = Option.objects.all()
        niveaus = Niveau.objects.all()
        fonc = CustomUser.objects.get(id=users)
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
                print("auteur")
        return render(request, 'auteurs/question.html',{'email':email,'img':img,'niveaus':niveaus,'option':option,'questions':questions,'chap_liste':chap_liste,'type_question':type_question,'form':form,'form2':form2})
def getdetails(request):
    #country_name = request.POST['country_name']
    chapitre_name = request.GET['cnt']
    print ("ajax country_name ", chapitre_name)

    result_set = []
    all_cities = []
    answer = str(chapitre_name)
    print(answer)
    selected_chapitre = Chapitre.objects.get(nom_chapitre=answer)
    print(selected_chapitre)
    print("selected country name ", selected_chapitre)

    all_cities = Lesson.objects.filter(chapitreid=selected_chapitre.id)
    print(all_cities)
    for city in all_cities:
        print(city.nom_lesson)
        result_set.append({'name': city.nom_lesson})
    return HttpResponse(simplejson.dumps(result_set),    content_type='application/json')

#page type question
def question_answer(request):
    question = Question.objects.all()

    return render(request, 'registration/corrige_form.html',{'question':question})

#choix option
def option_page(request,id):
    question = get_object_or_404(Question, id=id)
    question_text=question.question_texte
    question_id=str(question.id)
    chek=request.POST.getlist('check')
    print(chek)
    session = SessionEvaluationForm()
    for reponse in chek:
        print(reponse)
        sessions = session.save(commit=False)
        sessions.reponse=(question_id+":"+reponse)
        sessions.save()
    options = Option.objects.all()
    mesoption=OptionQuestion.objects.filter(question_id=question)
    liste=[]
    for option in mesoption:
        for opt in options:
            if option.option_id==opt.id:
                liste.append(opt.libelle)

    return render(request, 'registration/option_page.html',{'question_text':question_text,'question_id':question_id,'liste':liste})

#creer evaluation
def evaluation(request):
    return render(request, 'registration/evaluation.html')

#creer une interrogation
def interrogation(request,id):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        chapitre = Chapitre.objects.get(id=id)
        print(chapitre)
        a = chapitre.id
        auteur=request.user
        chek = request.POST.getlist('check')
        print(chek)
        conn = db.connect(host="localhost", user="root", password="", database="formation")
        cur = conn.cursor()
        liste_ques=[]
        liste_quesf=[]
        for rep in chek:
            questions=Question.objects.filter(lesson_id=rep)
            for que in questions:
                if que in liste_ques:
                    pass
                else:
                    liste_ques.append(que.id)
                for op in liste_ques:
                    opquestion=OptionQuestion.objects.filter(question_id=op)
                    for opq in opquestion:
                        if opq.question_id in liste_quesf:
                            pass
                        else:
                            liste_quesf.append(opq.question_id)
        print('liste des question des lesson ',liste_ques)
        print('liste des  question de l evaluation ', liste_quesf)
        print('les lesson',chek)
        b=request.POST['interne']
        print(b)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.types="Interrogation"
            if int(b)>0:
                evaluation.interne=1
            else:
                evaluation.interne=0
            evaluation.user_id=auteur.id
            evaluation.typeId=chek
            evaluation.save()
            x=evaluation.id
            for qu in liste_quesf:
                try:
                    cur.execute("INSERT INTO oorax_questionevaluation (evaluation_id,question_id)  VALUES (%s,%s) ",
                                [x,qu])
                    conn.commit()
                except:
                    # Rollback in case there is any error
                    conn.rollback()
            return redirect('interrogation',id=a)
    else:
        cour =Cour.objects.get(id=id)
        chapitre = Chapitre.objects.filter(courid_id=cour.id)
        lesson = Lesson.objects.all()
        evalu=Evaluation.objects.all()
        liste_eva=[]
        for eva in evalu:
            for x in eva.typeId:
                liste_eva.append(x)

        a = cour.id
        liste_chap=[]
        for cha in chapitre:
            for less in lesson:
                if cha.id is less.chapitreid_id:
                    liste_chap.append(less.id)
        print(liste_eva)

        form = EvaluationForm()
        return render(request,'auteurs/interro_form.html',{'form':form ,'a':a,
                                                                'liste_eva':liste_eva,
                                                                'evalu':evalu,
                                                                'liste_chap':liste_chap,'lesson':lesson})

#faire une interro
def faire_interro(request,id):
    evaluation = Evaluation.objects.get(id=id)
    a = evaluation.id
    liste_quest=[]
    queseva=QuestionEvaluation.objects.filter(evaluation_id=a)
    for ques in queseva:
        liste_quest.append(ques.question_id)
    print('liste des ques',liste_quest)
    final_liste=[]

    optEva = Option.objects.all()
    quesevalu = QuestionEvaluation.objects.all()
    questionoption = OptionQuestion.objects.all()
    question=Question.objects.all()
    form = EvaluationForm()
    hazzare=random.sample(liste_quest,2)
    return render(request, 'registration/evaluation.html',
                  {'optEva':optEva,
                   'quesevalu':quesevalu,
                   'questionoption':questionoption,
                   'question':question,
                   'final_liste':final_liste,
                   'hazzare':hazzare,
                   'form':form ,'a':a})

#envoi des reponses de l'interro
def envoi_evaluation(request):
    if request.method == 'POST':
        chek = request.POST.getlist('check')
        liste_chek=[]
        liste_opt=[]
        liste_lop=[]
        questt=[]
        evax=[]
        users = request.user
        evalus = SessionEvaluationForm()
        evalu = evalus.save(commit=False)
        #je recupere la liste des reponse fauses
        for ch in chek:
            options=OptionQuestion.objects.filter(option_id=ch)
            for qts in options:
                if qts.question_id in liste_chek:
                    pass
                else:
                    liste_chek.append(qts.question_id)
            for qts in liste_chek:
                qteva=QuestionEvaluation.objects.filter(question_id=qts)
                for evaid in qteva:
                    evax.append(evaid.evaluation_id)
                    print(evax)

            for opts in options:
                if opts.juste==0:
                    liste_opt.append(opts.option_id)
                
            if len(liste_opt)==0:
                evalu.point=(100)
                liste_lop.append(100)
            else:
                for faux in liste_opt:
                    listefaux = OptionQuestion.objects.filter(option_id=faux)
                    for f in listefaux:
                        if f.question_id in questt:
                            pass
                        else:
                            questt.append(f.question_id)
            if len(liste_chek)==len(questt):
                evalu.point=0
                liste_lop.append(0)
            else:
                points=(len(liste_chek)-len(questt))
                x=int(((points/len(liste_chek))*100))
                liste_lop.append(x)
                evalu.point=x



        point=evalu.point
        print("liste questions evaluation",liste_chek)
        print("liste questions evaluation faux", questt)
        evalu.userid_id=users.id
        evalu.reponse=chek
        #evalu.evaluation=evax
        evalu.save()
        eva=evalu.id
        return render(request, "registration/resultat.html", {'eva':eva,'point':point})
    else:

        return render(request, "registration/resultat.html" )

#__envoi des reponse de l'interro
def __envoi_evaluation(request):
    if request.method == 'POST':
        chek = request.POST.getlist('checks')
        liste_chek = []
        liste_opt = []
        liste_lop = []
        questt = []
        evax = []
        users = request.user
        evalus = SessionEvaluationForm()
        evalu = evalus.save(commit=False)
        # je recupere la liste des reponse fauses
        for ch in chek:
            options = OptionQuestion.objects.filter(option_id=ch)
            for qts in options:
                if qts.question_id in liste_chek:
                    pass
                else:
                    liste_chek.append(qts.question_id)
            for qts in liste_chek:
                qteva = QuestionEvaluation.objects.filter(question_id=qts)
                for evaid in qteva:
                    evax.append(evaid.evaluation_id)
                    print(evax)

            for opts in options:
                if opts.juste == 0:
                    liste_opt.append(opts.option_id)

            if len(liste_opt) == 0:
                evalu.point = (100)
                liste_lop.append(100)
            else:
                for faux in liste_opt:
                    listefaux = OptionQuestion.objects.filter(option_id=faux)
                    for f in listefaux:
                        if f.question_id in questt:
                            pass
                        else:
                            questt.append(f.question_id)
            if len(liste_chek) == len(questt):
                evalu.point = 0
                liste_lop.append(0)
            else:
                points = (len(liste_chek) - len(questt))
                x = int(((points / len(liste_chek)) * 100))
                liste_lop.append(x)
                evalu.point = x

        point = liste_lop[0]
        print("liste questions evaluation", liste_chek)
        print("liste questions evaluation faux", questt)
        evalu.userid_id = users.id
        evalu.reponse = chek
        # evalu.evaluation=evax
        evalu.save()
        return render(request, "registration/resultat.html", {'point': point})
    else:

        return render(request, "registration/resultat.html")


#afficher statistque uses
def stat_users(request):
    if request.method == 'POST':
        cour=request.POST["courid"]
        chapitres=request.POST["chapitreid"]
        lessons = request.POST["lessonid"]
        session = QuestionEvaluation.objects.all()
        if lessons:
            lesson = Lesson.objects.get(nom_lesson=lessons)
            less = lesson.id
            question = Question.objects.filter(lesson_id=less)
            print('mes lessons',less)
            liste_question = []
            liste_evalu = []
            questioneva = QuestionEvaluation.objects.all()
            if less:
                for x in question:
                    if x.id in liste_question:
                        pass
                    else:
                        liste_question.append(x.id)
                    for z in questioneva:
                        for y in liste_question:
                            if z.question_id is y:
                                if z.evaluation_id in liste_evalu:
                                    pass
                                else:
                                    liste_evalu.append(z.evaluation_id)
            users = request.user
            sesseva = SessionEvaluation.objects.filter(userid_id=users.id)
            return render(request, 'registration/stat_users.html',{'liste_evalu': liste_evalu, 'sesseva': sesseva})
        elif chapitres:
            question2 = Question.objects.all()
            questioneva = QuestionEvaluation.objects.all()
            chapitre = Chapitre.objects.get(nom_chapitre=chapitres)
            chap = chapitre.id
            lesso = Lesson.objects.filter(chapitreid_id=chap)
            print('mon chap', chap)
            liste_lesso = []
            liste_quest = []
            liste_evalu = []
            for l in lesso:
                for a in question2:
                    if l.id is a.lesson_id:
                        liste_quest.append(a.id)
                        for d in questioneva:
                            for c in liste_quest:
                                if d.question_id is c:
                                    if d.evaluation_id in liste_evalu:
                                        pass
                                    else:
                                        liste_evalu.append(d.evaluation_id)
                print('liste evaluation', liste_evalu)
                print('liste des lesson', liste_quest)
                users = request.user
                sesseva = SessionEvaluation.objects.filter(userid_id=users.id)
                return render(request, 'registration/stat_users.html', {'liste_evalu': liste_evalu, 'sesseva': sesseva})
        else:
            if cour:
                liste_evalu=[]
                chapitres = Chapitre.objects.filter(courid_id=cour)
                for cha in chapitres:
                    lesson=Lesson.objects.filter(chapitreid_id=cha.id)
                    for les in lesson:
                        questions=Question.objects.filter(lesson_id=les.id)
                        for ques in questions:
                            for sess in session:
                                if ques.id is sess.question_id:
                                    if sess.evaluation_id in liste_evalu:
                                        pass
                                    else:
                                        liste_evalu.append(sess.evaluation_id)
            print('liste evaluation', liste_evalu)
            users = request.user
            sesseva = SessionEvaluation.objects.filter(userid_id=users.id)
            return render(request, 'registration/stat_users.html', {'liste_evalu': liste_evalu, 'sesseva': sesseva})

    else:
        table=[]
        users=request.user
        sesseva=SessionEvaluation.objects.filter(userid_id=users.id)
        opquest = OptionQuestion.objects.all()
        questioneva = QuestionEvaluation.objects.all()
        question = Question.objects.all()
        option = Option.objects.all()
        lesson=Lesson.objects.all()
        chapitre=Chapitre.objects.all()
        evaluation=Evaluation.objects.all()
        cour=Cour.objects.all()
        return render(request, 'registration/stat_users.html',
                      {'evaluation':evaluation,
                       'cour':cour,
                       'chapitre':chapitre,
                       'lesson':lesson,
                       'table':table,
                       'option':option,'question':question,
                       'questioneva':questioneva,'sesseva':sesseva,'opquest':opquest})

def cherchap(request):
    #country_name = request.POST['country_name']
    chapitre_name = request.GET['cnt']
    print ("ajax country_name ", chapitre_name)
    result_set = []
    all_cities = []
    answer = str(chapitre_name)
    print(answer)
    selected_chapitre = Cour.objects.get(titre=answer)
    print(selected_chapitre)
    print("selected country name ", selected_chapitre)
    all_cities = Chapitre.objects.filter(courid_id=selected_chapitre.id)
    print(all_cities)
    for city in all_cities:
        print(city.nom_chapitre)
        result_set.append({'name': city.nom_chapitre})
    return HttpResponse(simplejson.dumps(result_set),    content_type='application/json') 
def cherless(request):
    # country_name = request.POST['country_name']
    chapitre_name = request.GET['cnt']
    print("ajax country_name ", chapitre_name)

    result_set = []
    all_cities = []
    answer = str(chapitre_name)
    print(answer)
    selected_chapitre = Chapitre.objects.get(nom_chapitre=answer)
    print(selected_chapitre)
    print("selected country name ", selected_chapitre)

    all_cities = Lesson.objects.filter(chapitreid=selected_chapitre.id)
    print(all_cities)
    for city in all_cities:
        print(city.nom_lesson)
        result_set.append({'name': city.nom_lesson})
    return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

#daatails statistique
def details(request,id):
    #questeva=QuestionEvaluation.objects.filter(evaluation_id=id)
    sessioneva = SessionEvaluation.objects.filter(id=id)
    optiqujust=OptionQuestion.objects.all()
    users=request.user
    liste_question=[]
    liste_option=[]
    a=0
    #for qeva in questeva:
     #   liste_question.append(qeva.question_id)

    for x in sessioneva:
        if x.userid_id==users.id:
            for y in x.reponse:
                liste_option.append(y)

    for z in liste_option:
        optquest = OptionQuestion.objects.filter(option_id=z)
        for op in optquest:
            if op.question_id in liste_question:
                pass
            else:
                liste_question.append(op.question_id)

    optquests = OptionQuestion.objects.all()
    option=Option.objects.all()
    question=Question.objects.all()
    print('liste des options', liste_option)
    print('liste des questions de leva selectionné',liste_question)
    return render(request, 'registration/detail_stat.html',
                  {'option':option,'optquests':optquests,
                   'a':a,
                   'optiqujust':optiqujust,'question':question,
                   'sessioneva':sessioneva,
                   'liste_question':liste_question})

def glisser(request):
    if request.method == 'POST':
        chek = request.POST.getlist('check')
        print(chek)
        chapi=[]
       # chapp = ChapitreForm()
        #chape = chapp.save(commit=False)
        chapitre = Chapitre.objects.filter(courid_id=3)
        for cha in chapitre:
            chapi.append(cha.id)

        i=0
        if len(chapi)>i:
            while len(chapi)>i:
                if int(chek[i])==int(chapi[i]):
                    print(chek[i],'==',chapi[i])
                    pass
                else:
                    print(chek[i], '!=', chapi[i])
                    chapitre = Chapitre.objects.get(id=chek[i])
                    chapitre.ordre='2'
                    chapitre.save()

                    chapitre = Chapitre.objects.get(id=chapi[i])
                    chapitre.ordre = '3'
                    chapitre.save()
                i = i + 1
        else:
            print('finich')


        #for check in chek:
         #   for cha in chapitre:
          #      if cha.id == check:
           #         print(check,'=',cha.id,'ok')
            #    else:
             #       print(check,'!=',cha.id,'no')
    i=0
    chapitre = Chapitre.objects.filter(courid_id=3)

    return render(request, 'registration/glisser_deposer.html',{'chapitre':chapitre,'i':i,})

#mes cours
def mes_cours(request):
    actu_user=request.user
    actu_user_id=actu_user.id
    print(actu_user_id)
    form = CourForm(request.POST, request.FILES)
    cour = Cour.objects.filter(auteur_id=actu_user_id)
    liste_transact=[]
    page = request.GET.get('page', 1)
    paginator = Paginator(cour, 10)
    try:
        cours = paginator.page(page)
    except PageNotAnInteger:
        cours = paginator.page(1)
    except EmptyPage:
        cours = paginator.page(paginator.num_pages)

    fonc = CustomUser.objects.get(id=actu_user_id)
    if fonc.fonction == 'Auteurs':
        email = fonc.email
        if fonc.image:
            img = fonc.image.url
        else:
            img = "pas d'image"
        transaction = Transaction.objects.filter(Q(libelle='Achat') & Q(user_sortie_id=actu_user_id))
        inscription = Inscription.objects.all()
        categories = Categorie.objects.all()
        domaine = Domaine.objects.all()
        return render(request, 'auteurs/mes_cours.html',{'domaine':domaine,'form':form,'categories':categories,'cours':cours,'transaction':transaction,'inscription':inscription,'email':email,'img':img})
    else:
        domaine = Domaine.objects.all()
        transaction = Transaction.objects.filter(Q(libelle='Achat') & Q(user_sortie_id=actu_user_id))
        inscription = Inscription.objects.all()
        categories = Categorie.objects.all()
        return render(request, 'registration/mes_cours.html',
                      {'categories': categories, 'domaine':domaine,'form':form,'cours': cours, 'transaction': transaction,
                       'inscription': inscription,})


#contenu du cour
def contenu_mes_cours(request,id):
    cour = Cour.objects.get(id=id)
    lesson=Lesson.objects.all()
    eleve=request.user.id
    print(eleve)
    chapis=[]
    chas=[]
    liste_less=[]
    poin_lt = []
    liste_eva = []
    dernier_point = []
    che_point = []
    cha_liste=[]
    l=0
    ca=0
    tout=0
    cour_id=cour.id
    cour_titre=cour.titre
    cour_auteur=cour.auteur
    sessevalu=SessionEvaluation.objects.all()
    evalua = Evaluation.objects.all()
    chapeva=ChapEvaluation.objects.all()
    chapitre = Chapitre.objects.filter(courid_id=cour_id)
    users=CustomUser.objects.all()

    while len(chapitre)>tout:
        print('chapitre',tout)

        for less in Lesson.objects.all():
            if less.chapitreid_id is chapitre[tout].id:
                liste_less.append(less.id)

        print(liste_less)
        for evas in evalua:
            for r in liste_less:
                if r in evas.typeId:
                    liste_eva.append(evas.id)

        print(liste_eva)
        if sessevalu:
            for sess in sessevalu:
                if sess.evaluation_id in liste_eva and sess.userid_id is eleve:
                    poin_lt.append(sess.point)
                    print('point', poin_lt, sess.evaluation_id)


            while len(liste_less) > l:
                if poin_lt[-1] >= 90:
                    print('vous avez 90 %', poin_lt[-1], 'taille',len(liste_less))
                    l = l + 1
                else:
                    print('vous n avez pas 90%',poin_lt[-1])

                    for se in sessevalu:
                        if se.point is poin_lt[-1]:
                            a=se.evaluation_id
                            print('eva',a)
                    contenu = Contenue.objects.all()
                    return render(request, 'registration/contenu_mes_cours.html',
                                  {'contenu': contenu, 'lesson': lesson,
                                   'chapitre': chapitre,
                                   'cour_titre': cour_titre,
                                   'cour_auteur': cour_auteur, 'a': a}
                                  )

                if len(liste_less) > l:
                    print('lesson',l)
                    for eva in evalua:
                        if liste_less[l] in eva.typeId:
                            a = eva.id
                            print('evaggg', a, liste_less[-1])
                            for sessi in sessevalu:
                                if liste_less[-1] is liste_less[l]:
                                    p = sessi.point
                                    if p >= 90:
                                        if chapeva:
                                            for chap in chapeva:
                                                if chap.chapitreid_id is chapitre[tout].id:
                                                    che_point.append(chap.point)

                                            print('faire',che_point)
                                            if len(che_point)>=3:
                                                for d in che_point[-3:]:
                                                    dernier_point.append(d)
                                                somm = dernier_point.count(30)
                                                if somm>=3:

                                                    print('ev', a, tout)
                                                    contenu = Contenue.objects.all()

                                                print('somme', somm)
                                                break

                                            else:
                                                print('faire encore')
                                                print('chapitre suivant',chapitre[tout].id)
                                                chapi=chapitre[tout].id
                                                return render(request, 'registration/evalu_chapitre.html',
                                                              {
                                                                  'chapi': chapi, }
                                                              )
                                        else:
                                            if somm>=3:
                                                pass
                                            else:
                                                print('vide')
                                                chapi = chapitre[tout].id
                                                return render(request, 'registration/evalu_chapitre.html',
                                                              {
                                                                  'chapi': chapi, }
                                                              )
                                else:
                                    print('cest pas fini')
                else:
                    print('yyyyyy')

            liste_eva[:] = []
            liste_less[:] = []


        tout = tout + 1

# fiche d'evaluation
def chap_evalua(request,id):
    chapitre = Chapitre.objects.get(id=id)
    a=chapitre.id
    print(a)
    questions=Question.objects.all()
    lessons=Lesson.objects.all()
    quest_liste=[]
    less_liste = []
    for less in lessons:
        if less.chapitreid_id is a:
            less_liste.append(less.id)

    print('lesson ', less_liste)
    for quest in questions:
        if quest.lesson_id in less_liste:
            print('question',quest.lesson_id)
            quest_liste.append(quest.id)

    optEva = Option.objects.all()
    quesevalu = QuestionEvaluation.objects.all()
    questionoption = OptionQuestion.objects.all()
    form = EvaluationForm()
    hazzare = random.sample(quest_liste, 2)
    return render(request, 'registration/chap_evalua.html',
                  {'optEva': optEva,
                   'quesevalu': quesevalu,
                   'questionoption': questionoption,
                   'questions': questions,
                   'hazzare': hazzare, 'quest_liste': quest_liste,
                   'form': form, 'a': a})


# envoi des reponses de l'evalution chap
def envoi_evaluation_chap(request):
    if request.method == 'POST':
        chek = request.POST.getlist('check')
        liste_chek = []
        liste_opt = []
        liste_lop = []
        questt = []
        users = request.user
        lessons=Lesson.objects.all()
        evalus = ChapEvaluationForm()
        chapitre=Chapitre.objects.all()
        evalu = evalus.save(commit=False)
        # je recupere la liste des reponse fauses
        evax=[]
        questions = Question.objects.all()
        for ch in chek:
            options = OptionQuestion.objects.filter(option_id=ch)
            for qts in options:
                if qts.question_id in liste_chek:
                    pass
                else:
                    liste_chek.append(qts.question_id)
            print('1')
            for qts in questions:
                if qts.id in liste_chek:
                    evax.append(qts.lesson_id)
            print(evax)
            y=[]
            for z in lessons:
                if z.id in evax:
                    y.append(z.chapitreid_id)
                    print('mes reponses',z,y)

            for c in chapitre:
                if c.id in y:
                    cha=c.id


            for opts in options:
                if opts.juste == 0:
                    liste_opt.append(opts.option_id)

            if len(liste_opt) == 0:
                evalu.point = (100)
            else:
                for faux in liste_opt:
                    listefaux = OptionQuestion.objects.filter(option_id=faux)
                    for f in listefaux:
                        if f.question_id in questt:
                            pass
                        else:
                            questt.append(f.question_id)
            if len(liste_chek) == len(questt):
                evalu.point = 0
            else:
                points = (len(liste_chek) - len(questt))
                x = int(((points / len(liste_chek)) * 100))
                evalu.point = x

        print("liste questions evaluation", liste_chek)
        print("liste questions evaluation faux", questt)
        evalu.userid_id = users.id
        evalu.reponse = chek
        evalu.userid_id=users.id
        evalu.chapitreid_id = cha
        evalu.save()

        return HttpResponse('reponse envoyé')

    return render(request, "registration/home.html", )

def sexion_quiz(request):
    actu_user = request.user
    actu_user_id = actu_user.id
    print(actu_user_id)
    cour = Cour.objects.all()
    liste_transact = []
    objects_list = []
    for row in cour:
        d = collections.OrderedDict()
        d['id'] = row.id
        d['Titre'] = row.titre
        d['Prix'] = row.prix
        d['Description'] = row.description
        d['Auteur'] = row.auteur_id
        objects_list.append(d)
    j = simplejson.dumps(objects_list)
    with open("fichierJson.js", "w") as f_write:
        simplejson.dump(objects_list, f_write)

    transaction = Transaction.objects.filter(Q(libelle='Achat') & Q(user_sortie_id=actu_user_id))
    inscription = Inscription.objects.all()
    return render(request, 'registration/sexion_quiz.html',
                  {'cour': cour, 'transaction': transaction, 'inscription': inscription})

def mes_quiz(request,id):
    cour = Cour.objects.get(id=id)
    cour_id=cour.id
    cour_titre=cour.titre
    chapitre = Chapitre.objects.filter(courid_id=cour_id)
    users=CustomUser.objects.all()
    contenu = Contenue.objects.all()
    return render(request, 'registration/chapitre_mes_cour.html',
                    {'contenu': contenu,
                    'chapitre': chapitre,
                     'cour_titre':cour_titre,})

def choix_quiz(request):
    chek = request.POST.getlist('check')
    cheker = Check.objects.filter(id=1)
    question = Question.objects.all()
    print(chek)
    liste_less=[]
    liste_quest=[]
    i=0
    a = []
    lesson=Lesson.objects.all()
    question=Question.objects.all()
    while len(chek)>i:
        for less in lesson:
            if int(chek[i]) is less.chapitreid_id:
                liste_less.append(less.id)
        for quest in question:
            for y in liste_less:
                if quest.lesson_id is y:
                    liste_quest.append(quest.id)
        if len(chek)>=i:
            hazzare = random.sample(liste_quest, 5)
            pass
        else:
            print('fin')

        a=a+hazzare
        print(a)
        print('lesson',chek[i], liste_less,liste_quest)
        liste_less[:]=[]
        liste_quest[:] = []
        i=i+1
    optEva = Option.objects.all()
    quesevalu = QuestionEvaluation.objects.all()
    questionoption = OptionQuestion.objects.all()
    question = Question.objects.all()
    return render(request, 'registration/choix_quiz.html',
    {'optEva': optEva,
     'quesevalu': quesevalu,
     'questionoption': questionoption,
     'question': question,
     'a': a,
     'cheker':cheker,
     'question':question,
     }
    )

def check(request):
    if request.method == 'POST':
        chek1 = request.POST.getlist('less')
        chek2 = request.POST.getlist('less2')
        chek3 = request.POST.getlist('less3')
        explic=[int(i) for i in chek1]
        print(explic)
        temps=[int(o) for o in chek2]
        print(temps)

        cheker=Check.objects.filter(id=1)

        if 0 in explic:
            x = False
        else:
            x = True
        if 0 in temps:
            z = False
        else:
            z = True

        for y in cheker:
            y.check = x
            y.temps = z
            y.save()

        print('chek1',chek1)
        print('chek2',chek2)
        print('chek3',chek3)

        return redirect('index')

#mon profil
def view_profile(request):
    users = request.user.id
    if users:
        fonc = CustomUser.objects.get(id=users)
        if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
            b = 1
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
            print("auteur")

            var1 = Transaction.objects.filter(user_sortie_id=users)
            var2 = Transaction.objects.filter(user_entree_id=users)
            x = 0
            y = 0
            for trans in var1:
                x = x + trans.montant
            for tran in var2:
                y = y + tran.montant
            soldes = int(y - x)
            solde = '{:,}'.format(soldes)
            # solde=float(soldesString.replace(',', '.'))
            print('mon solde est', solde)


            return render(request, 'auteurs/profile.html', { 'solde': solde,
                                                             'email': email, 'img': img,})

        elif fonc.fonction == 'Apprenants' and fonc.email_validated == 1:
            b = 0
            email = fonc.email
            if fonc.image:
                img = fonc.image.url
            else:
                img = "pas d'image"
            return render(request, 'registration/profile.html')
    else:
        return HttpResponse('connectez-vous?')

def domaine(request):
    if request.method == 'POST':
        form = DomaineForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return  HttpResponse('ok')
    else:
        form = DomaineForm()
        return render(request, 'registration/domaine.html', {'form': form})


def cour_details(request,id):
    cour = Cour.objects.get(id=id)
    cour_id = cour.id
    cour_titre = cour.titre
    cour_description=cour.description
    cour_image=cour.image
    cour_auteur=cour.auteur_id
    users=CustomUser.objects.get(id=cour_auteur)
    auteur=users.username
    cat=Categorie.objects.get(id=cour.categorieid_id)
    cour_categorie = cat.nom_categorie
    dom=Domaine.objects.get(id=cour.domaineid_id)
    cour_domaine =dom.nom_domaine

    inscrip = Inscrit.objects.all()
    liste_inscri = []
    for ins in inscrip:
        liste_inscri.append(ins.cour_id)
    return render(request, 'registration/cour_detail.html',
                  {'auteur':auteur,'cour_image':cour_image,'cour_titre':cour_titre,
                   'cour_description':cour_description,'cour_categorie':cour_categorie,
                   'liste_inscri':liste_inscri,'cour_domaine':cour_domaine,'cour_id':cour_id})

#les cour de l'utilisateur
def user_mes_cours(request):
    actu_user = request.user
    actu_user_id = actu_user.id
    list_cour=[]
    print(actu_user_id)
    inscrip=Inscrit.objects.filter(custom_id=actu_user_id)
    lesson=Lesson.objects.all()
    chapitre=Chapitre.objects.all()
    cour = Cour.objects.all()
    var1 = Transaction.objects.filter(user_sortie_id=actu_user.id)
    var2 = Transaction.objects.filter(user_entree_id=actu_user.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(cour, 15)
    try:
        cours = paginator.page(page)
    except PageNotAnInteger:
        cours = paginator.page(1)
    except EmptyPage:
        cours = paginator.page(paginator.num_pages)
    x = 0
    y = 0
    for trans in var1:
        x = x + trans.montant
    for tran in var2:
        y = y + tran.montant
    soldes = int(y - x)
    solde = '{:,}'.format(soldes)

    for ins in inscrip:
        for c in cours:
            if ins.cour_id is c.id:
                list_cour.append(c.id)

    print(list_cour)
    fonc = CustomUser.objects.get(id=actu_user_id)
    if fonc.fonction == 'Auteurs':
        email = fonc.email
        if fonc.image:
            img = fonc.image.url
        else:
            img = "pas d'image"
        categories = Categorie.objects.all()
        checked = Check.objects.filter(id=1)
        return render(request, 'auteurs/user_mes_cours.html',
                      {'list_cour':list_cour,'categories': categories,'checked': checked,'solde':solde, 'cours': cours,'email':email,'img':img})
    else:
        categories = Categorie.objects.all()
        checked = Check.objects.filter(id=1)
        return render(request, 'registration/user_mes_cours.html',
                      {'list_cour': list_cour, 'checked': checked,'categories': categories, 'cours': cours})

#detai_user_mes_cours
def detail_user_cour(request,id):
    cour = Cour.objects.get(id=id)
    us=request.user
    cour_id = cour.id
    cour_titre = cour.titre
    cour_description = cour.description
    cour_image = cour.image
    cour_auteur = cour.auteur_id
    users = CustomUser.objects.get(id=cour_auteur)
    auteur=users.username
    lesson = Lesson.objects.all()
    contenu = Contenue.objects.all()
    chapitre = Chapitre.objects.filter(courid_id=cour_id)
    chapitres = Chapitre.objects.all()
    cat = Categorie.objects.get(id=cour.categorieid_id)
    cour_categorie = cat.nom_categorie
    dom = Domaine.objects.get(id=cour.domaineid_id)
    insc=Inscription.objects.filter(users_id=us.id)
    list_chap=[]
    list_less=[]
    for u in insc:
        list_less.append(u.cour_id)
        for l in lesson:
            if u.cour_id is l.id:

                list_chap.append(l.chapitreid_id)

    fonc = CustomUser.objects.get(id=us.id)
    if fonc.fonction == 'Auteurs' and fonc.email_validated == 1 or fonc.is_superuser:
        b = 1
        email = fonc.email
        if fonc.image:
            img = fonc.image.url
        else:
            img = "pas d'image"
    print('liste chap',list_chap)
    cour_domaine = dom.nom_domaine
    return render(request, 'auteurs/detail_user_cour.html',
                  {'auteur':auteur,'contenu':contenu,'lesson':lesson, 'chapitre': chapitre,
                   'cour_image': cour_image, 'cour_titre': cour_titre,'list_chap':list_chap,
                   'cour_description': cour_description, 'cour_categorie': cour_categorie,'email':email,
                   'cour_domaine': cour_domaine,'chapitres': chapitres,'list_less':list_less,'img':img })


#new mode evaluation
def choix_question(request):
    if request.method == 'POST':
        chek = request.POST.getlist('check')
        result = [int(i) for i in chek]

        quest=Question.objects.all()
        quest_list=[]
        less_list=[]
        for qu in quest:
            less_list.append(qu.lesson_id)
            if qu.lesson_id in result:
                quest_list.append(qu.id)
            else:
                pass

        optEva = Option.objects.all()
        quesevalu = QuestionEvaluation.objects.all()
        questionoption = OptionQuestion.objects.all()
        question = Question.objects.all()
        hazzare = random.sample(quest_list, 3)
        print('liste des questions :', hazzare)
        parram=Check.objects.all()
        for par in parram:
            active=par.check
            active2=par.temps
            if active is True:
                act = 1
                act2 = 0
            elif active2 is True:
                act = 0
                act2 = 1
            else:
                act = 0
                act2 = 0



    return render(request, 'registration/choix_quiz.html',
                  {'optEva': optEva,
                   'quesevalu': quesevalu,
                   'hazzare':hazzare,
                   'questionoption': questionoption,
                   'question': question,
                   'question': question,
                   'act':act,
                   'act2': act2,

                   }
                  )

#autorisation auteur
def activation_liste(request,id):
    users = CustomUser.objects.get(id=id)
    if users.email_validated==True:
        return HttpResponse('email deja validé')
    else:
        users.email_validated=True
        users.save()
        return redirect('administrer')

#blocker utilisateur
def block_liste(request,id):
    users = CustomUser.objects.get(id=id)
    if users.blocker==True:
        return HttpResponse('deja blocké')
    else:
        users.blocker=False
        print('false')
        users.save()
        print(users.save())

        
        return redirect('administrer')


def white_liste(request,id):
    users = CustomUser.objects.get(id=id)
    if users.blocker == False:
        return HttpResponse('deja dblocké')
    else:
        users.blocker = True
        users.save()
        return redirect('administrer')