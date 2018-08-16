import json as simplejson
from pyquery import PyQuery as pq
import postmarkup
import bbcode
from html.parser import HTMLParser
from precise_bbcode.bbcode import get_parser
from django.contrib.auth.views import logout
from django.http import HttpResponse, QueryDict
import MySQLdb as db
import random
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
from django.utils import text

# Create your views here.

#page d'accueil
def index(request):
    parser = bbcode.Parser()
    code = "[s]a = [1, 2, 3, 4, 5][/s]"
    plain_txt = parser.strip(code)
    print(plain_txt)
    #parser = get_parser()
    #rendered = parser.render('[b]Hello [u]world![/u][/b]')
    #print(rendered)
    #h = HTMLParser()
    #print(h.unescape('<strong>huiz</strong>'))
    #markup = postmarkup.PostMarkup().default_tags()
    #bbcode = "[b]Hello, World![/b]"
    #print(markup.render(bbcode))
    return render(request, 'registration/index.html')



def home(request):
    cours = Cour.objects.filter(etat_cour=0)
    categories = Categorie.objects.all()
    return render(request,'registration/home.html',{'cours':cours,'categories':categories})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'registration/login.html')
        else:
            redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})

# vue de la page activation de compte
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = False
        user.email_validated = True
        user.save()
        logout(request)
        return render(request, 'registration/login.html')
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

            cat = Categorie.objects.get(nom_categorie=nom_cat)
            print(cat.id)
            user = form.save(commit=False)
            user.categorieid_id = cat.id
            user.etat_cour=0

            user.save()
        categories = Categorie.objects.all()
        cours = Cour.objects.filter(etat_cour=0)
        return render(request, 'registration/cour_register_form.html',
                          {'form': form, 'categories': categories, 'cours': cours})

    else:
        form = CourForm()
        categories = Categorie.objects.all()
        cours = Cour.objects.filter(etat_cour=0)
    return render(request, 'registration/cour_register_form.html',{'form': form,'categories':categories,'cours':cours})

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
    return redirect('cour')

#Ajouter chapitre
def chapitre_cour(request,id):
    cour = Cour.objects.get(id=id)
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
        return render(request, "registration/chapitre_cour.html",
                      {'formless': formless,
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

                return redirect('contenu_lesson',id=lesson.id)
    else:
        form = ContenuForm()
        form2 = ContenuLienForm()
        contenu = Contenue.objects.filter(lessoneid_id=a)
        #parser = get_parser()
        print(postmarkup.parser.PostMarkup)
        #parser = bbcode.Parser()
        markup =postmarkup.parser.PostMarkup()
        #bbcode = "[b]Hello, World![/b]"

        for c in contenu:
            plain_txt = markup.render_to_html(c.contenu_texte)
        print('de la base de donnee',plain_txt)

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


        return render(request, "registration/contenu_cour.html",
                      {'form': form,
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
                        'plain_txt':plain_txt,
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
    return render(request, 'registration/compte_credit.html')

#page charger compte
def recharger_compte(request):

    if request.method == 'POST':
        form = RechargerForm(request.POST)
        form2 = Recharger2Form(request.POST)
        choix1=request.user
        print(choix1.identifiant)
        print(form)
        if form.is_valid():
            x=request.POST["ref"]
            print(x)
            if x==choix1.identifiant:
                users = form.save(commit=False)
                users.mobile_moneyId_id =request.POST["hide"]
                users.user_entree_id = choix1.id
                users.montant = 50000
                users.libelle = 'Chargement'
                users.save()
            return redirect('recharger_compte')
        return redirect('recharger_compte')
    else:
        form = RechargerForm()
        form2 = Recharger2Form()
        omoney = Mobilemoney.objects.all()
        return render(request, 'registration/recharger_compte.html',{'omoney':omoney,'form2':form2,'form':form})

#page transfert credi
def transfert_credit(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        users=request.user
        if form.is_valid():
            a = request.POST["ident"]#recuperer identifiant du recepteur
            m = request.POST["montant"]
            montant= int(m)
            lui = CustomUser.objects.filter(identifiant=a)#retrouver le recepteur
            var1 = Transaction.objects.filter(user_sortie_id=users)
            var2 = Transaction.objects.filter(user_entree_id=users)
            x = 0
            y = 0
            for trans in var1:
                x = x + trans.montant
            for tran in var2:
                y = y + tran.montant
            solde = int(y - x)
            for s in lui:
                print(s.identifiant)
            moi = request.user
            if s.identifiant and solde>montant:
                users = form.save(commit=False)
                users.user_sortie_id = moi.id
                users.user_entree_id = s.id
                users.reference = s.identifiant
                users.libelle = 'Transfert'
                users.save()
                return redirect('transfert_credit')
            return HttpResponse("solde insufisant")
    else:
        form = TransferForm()
        #user = CustomUser.objects.all()
        return render(request, 'registration/transfert_credit.html',{'form':form})

#page inscription
def inscription(request,id):
    cour = Cour.objects.get(id=id)
    #service = Service.object.all()

    id = cour.id
    titre=cour.titre
    prix=cour.prix
    return render(request, "registration/inscription.html",{'titre':titre,'prix':prix,'id':id})
def achat(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        users=request.POST["users"]#recuperer l'id du user
        courid=request.POST["courid"]#recuperer l'id du cour
        z = Cour.objects.get(id=courid)#retrouver l'id du cour
        var1 = Transaction.objects.filter(user_sortie_id=users)
        var2 = Transaction.objects.filter(user_entree_id=users)
        x = 0
        y = 0
        for trans in var1:
            x = x + trans.montant
        for tran in var2:
            y = y + tran.montant
        solde = int(y - x)
        if solde >= z.prix:
            usertrans=form.save(commit=False)
            usertrans.user_sortie_id = users
            usertrans.montant = z.prix
            usertrans.libelle = 'Achat'
            x = solde - z.prix
            usertrans.save()
            var3 = usertrans.id
            form2 = InscriptionForm()
            insc = form2.save(commit=False)
            insc.cour_id = courid
            insc.transaction_id = var3
            insc.save()
        return render(request, "registration/home.html", )
    form = TransferForm()
    return render(request, "registration/home.html",{'form':form})

#page historique
def historique(request):
    user1 = request.user
    var2 = Transaction.objects.filter(Q(user_entree_id=user1.id) | Q(user_sortie_id=user1.id))#recuperer les entrées=user.id OU sortie=user.id
    return render(request, 'registration/historique.html',{'var2':var2})

#page creer qustion
def question(request,id):
    if request.method == 'POST':
        form=QuestionForm(request.POST)
        users = request.user
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
            user.user_id=users.id
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
            return render(request, 'registration/question.html',
                          {'niveaus':niveaus,'option':option,
                           'chap_liste': chap_liste, 'type_question': type_question, 'form': form, 'questions':questions})
    else:
        form = QuestionForm()
        form2 = OptionForm()
        question = Cour.objects.get(id=id)
        questions = question.id
        chap_liste = Chapitre.objects.filter(courid_id=question.id)
        type_question = TypeQuestion.objects.all()
        option = Option.objects.all()
        niveaus = Niveau.objects.all()
        return render(request, 'registration/question.html',{'niveaus':niveaus,'option':option,'questions':questions,'chap_liste':chap_liste,'type_question':type_question,'form':form,'form2':form2})
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
        a = chapitre.id
        auteur=request.user
        chek = request.POST.getlist('check')
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
        chapitre = Chapitre.objects.get(id=id)
        a = chapitre.id
        print(a)
        lesson=Lesson.objects.filter(chapitreid_id=a)

        form = EvaluationForm()
        return render(request,'registration/interro_form.html',{'form':form ,'a':a, 'lesson':lesson})

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
    hazzare=random.sample(liste_quest,1)
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
                    evax=evaid.evaluation_id

            for opts in options:
                if opts.juste==0:
                    liste_opt.append(opts.option_id)
                
            if len(liste_opt)==0:
                evalu.point=(100)
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
            else:
                points=(len(liste_chek)-len(questt))
                x=int(((points/len(liste_chek))*100))
                evalu.point=x


        print("liste questions evaluation",liste_chek)
        print("liste questions evaluation faux", questt)
        evalu.userid_id=users.id
        evalu.reponse=chek
        evalu.evaluation_id=evax
        evalu.save()

        return HttpResponse('reponse envoyé')

    return render(request, "registration/home.html", )

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
    questeva=QuestionEvaluation.objects.filter(evaluation_id=id)
    sessioneva = SessionEvaluation.objects.filter(evaluation_id=id)
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
                   'questeva':questeva,'sessioneva':sessioneva,
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












