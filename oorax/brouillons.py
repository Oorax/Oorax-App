# con = MySQLdb.connect('localhost', 'root', '', 'formation');
# cur = con.cursor()
# cur.execute("SELECT montant FROM oorax_transaction where user_sortie_id=1 or user_entree_id=1")
# rows = cur.fetchall()


# var2 = Transaction.objects.filter(user_entree_id=1).query
# var1=Transaction.objects.extra(select={'items_count': 'SELECT montant FROM oorax_transaction WHERE user_entree_id = 1'})
# print(var1)


print(" ++++++++++++++++++++ ")
i = 0
print(i)
liste = []
# for option in my:
#   liste.append(option)
#  print(tuple(liste))
# conn = db.connect(host="localhost", user="root", password="", database="formation")
# cur = conn.cursor()
# cur.execute("""INSERT INTO oorax_option (libelle)  VALUES %(s)""", tuple(liste))

# query = "INSERT INTO oorax_option (libelle)  VALUES (%(libelle)s)"
# cur.executemany(query, tuple(liste))
# conn.close()

if len(my) > 0:
    while len(my) > i:
        opt.libelle = my[i]
        if opt.libelle == my[1]:
            print(opt.libelle)
            opt.save()
        else:
            opt.libelle = my[i]
            print(opt.libelle)
            opt.save()
        optionid = opt.id
        print(optionid)
        optquest = form3.save(commit=False)
        optquest.option_id = optionid
        optquest.question_id = quest_id
        optquest.save()
        i = i + 1

        for option in my:
            query = "INSERT INTO oorax_option (libelle)  VALUES (%s)"
            cur.execute(query, my)
            print("Auto Increment ID: %s" % cur.lastrowid)

            # i = 0

            # query = "INSERT INTO oorax_option (libelle)  VALUES (%s)"
            try:
                # cur.executemany(query,my)
                # conn.commit()
                # print("reuissite")
                if cur.lastrowid:
                    while i < len(my):
                        optionid = cur.lastrowid
                        print(optionid)
                        optquest = form3.save(commit=False)
                        optquest.option_id = optionid
                        optquest.question_id = quest_id
                        optquest.save()
                        i = i + 1
                print(i)

            except:
                # Rollback in case there is any error
                conn.rollback()
                print("echoué")






 for finalId in liste_opt:
            optEva = Option.objects.filter(id=finalId)
            for op in optEva:
                for oq in optionsquest:
                    if op.id==oq.option_id:
                        final_liste.append(op.libelle)
                        if oq.question_id in liste_id:

                            pass
                        else:
                            liste_id.append(oq.question_id)



{% if stat.evaluation_id is q.evaluation_id %}
                        {% for lis in opquest %}
                            {% if q.question_id is lis.question_id %}
                                {% for opt in option %}
                                    {% if lis.option_id is option.id %}
                                        <td>{{ lis.question_id }}</td>
                                        <td>{{ opt.id }}</td>
                                        <td>reponse C</td>
                                    {% endif %}
                                 {% endfor %}
                            {% endif %}
                        {% endfor %}
                    {% endif %}







<table border="1">
{% for stat in sesseva %}



	  <tr>
		<td rowspan="3">{{ stat.evaluation_id }}</td>
		<td>
            Evaluation
            <th>
                Date
            </th>

            <th>
                Points
            </th>

        </td>
	  </tr>
	  <tr>
		<td>
            <table border width =100%>
                <thead>
                    <tr>
                        <th>Questions</th>
                        <th>Reponses</th>
                        <th>Points</th>

                    </tr>
                </thead>

{% for q in questioneva %}

     {% for lis in opquest %}
                <tr>
                        {% if stat.evaluation_id is q.evaluation_id %}
                            {% if lis.question_id is q.question_id %}
                                {% for rep in stat.reponse %}
                                    {% if rep is lis.option_id %}
                                        {% for qt in question %}
                                            {% for op in option %}
                                                {% if qt.id is q.question_id %}
                                                    {% if op.id is rep %}
                                                        <td>{{ qt.question_texte }}</td>
                                                        <td>{{ op.libelle }}</td>
                                                        <td>points C</td>
                                                    {% endif %}
                                                {% endif %}
                                            {% endfor %}
                                        {% endfor %}
                                    {% endif %}
                                {% endfor %}

                            {% endif %}
                         {% endif %}

                </tr>
      {% endfor %}

    {% endfor %}
	        </table>

        </td>
        <td>{{ stat.date_evaluation }}</td>
        <td>{{ stat.point }}</td>
	  </tr>

{% endfor %}

	</table>


#pour faire evaluation

for evalu in evaluation:
    listEva.append(evalu.typeId)
    for l in evalu.typeId:
        li.append(l)
print(len(li))
while len(li) > i:
    for less in lesson:
        if less.id == li[i]:
            liste_choix.append(less.id)
    i = i + 1
for choix in liste_choix:
    # print(choix)
    question = Question.objects.filter(lesson_id=choix)
    for q in question:
        liste_question.append(q.id)
        liste_questexte.append(q.question_texte)

# ici je recupère les questions et les options
for quesId in liste_question:
    options = OptionQuestion.objects.filter(question_id=quesId)
    for o in options:

        if o.question_id in question_liste:
            pass
        else:
            question_liste.append(o.question_id)

        if o.option_id in liste_opt:
            pass
        else:
            liste_opt.append(o.option_id)

            liste_id = []
            for qt in question_liste:
                optionsquest = OptionQuestion.objects.filter(question_id=qt)
                for opti in optionsquest:
                    final_liste.append(opti.option_id)
                    # print('question',opti.option_id)

                optEva = Option.objects.all()

                { %
                for q in question %}
                { % if q.lesson_id is l.id %}
                < button > < a
                href = "{% url 'faire_interro' id=eva %}" > Evaluation
                {{eva}} < / a > < / button >
                < td > {{l.nom_lesson}} < / td >
                < td > < a
                href = "{% url 'contenu_lesson' l.id %}" > Ajouter
                Contenu < / a > | | < a
                href = "{% url 'lesson_edit' l.id %}" > Edit < / a > | | < a
                href = "{% url 'lesson_delete' l.id %}" > Delete < / a > < / td >

            { % else %}
            < td > {{l.nom_lesson}} < / td >
            < td > < a
            href = "{% url 'contenu_lesson' l.id %}" > Ajouter
            Contenu < / a > | | < a
            href = "{% url 'lesson_edit' l.id %}" > Edit < / a > | | < a
            href = "{% url 'lesson_delete' l.id %}" > Delete < / a > < / td >

    { % endif %}
    { % endfor %}

    < form
    name = "formulaireDynamique"
    id = "form" >
    < input
    type = "button"
    onclick = "ajout(this);"
    value = "ajouter un champ" / >
    < br / > < br / >

< / form >




<div class="container">

      <table border="1">




	  <tr>
        <th>N</th>
        <th>Questions</th>
        <th>Reponse</th>
        <th>Points</th>
	  </tr>
          {% for q in liste_question %}
             {% for opq in optquest %}
                {% if q is opq.question_id %}
                     {% for se in sessioneva %}
                        {% for rep in se.reponse %}
                            {% if opq.option_id is rep %}
                                {% for op in option %}
                                    {% if op.id is opq.option_id %}
                                      <tr>
                                          <td></td>
                                          <td>{{ q }}</td>
                                          <td>{{ op.libelle }}</td>
                                          <td>none</td>
                                      </tr>
                                    {% endif%}
                                {% endfor %}
                            {% endif%}
                        {% endfor %}
                     {% endfor %}
                {% endif%}
            {% endfor %}
          {% endfor %}


	</table>

</div> <br><br><br><br><br><br><br><br>

else:
if cour:
    questioneva = QuestionEvaluation.objects.all()
    chapitre = Chapitre.objects.get(nom_chapitre=chapitres)
    chap = chapitre.id
    lesso = Lesson.objects.filter(chapitreid_id=chap)
    print('mon chap', chap)
    liste_lesso = []
    liste_quest = []
    liste_evalu = []

    { %
    for l in lesson %}
    { %
    for eva in liste_evalu %}
    { %
    for qe in quesevalu %}
    { % if eva is qe.evaluation_id %}
    { %
    for q in question %}
    { % if qe.question_id is q.id %}

    < tr >
    < td > {{l.id}} < / td >
    { % if l.id is q.lesson_id %}

    < td > < button > < a
    href = "{% url 'faire_interro' id=eva %}" > Evaluation
    {{eva}} < / a > < / button > < / td >
    { % else %}
    < td > {{l.nom_lesson}} < / td >
    { % endif %}
    < td > < a
    href = "{% url 'contenu_lesson' l.id %}" > Ajouter
    Contenu < / a > | | < a
    href = "{% url 'lesson_edit' l.id %}" > Edit < / a > | | < a
    href = "{% url 'lesson_delete' l.id %}" > Delete < / a > < / td >

    < / tr >

    { % endif %}
    { % endfor %}
    { % endif %}
    { % endfor %}
    { % endfor %}
    { % endfor %}














    # a = chapitre.id
    auteur = request.user
    chek = request.POST.getlist('check')
    conn = db.connect(host="localhost", user="root", password="", database="formation")
    cur = conn.cursor()
    liste_ques = []
    liste_quesf = []
    for rep in chek:
        questions = Question.objects.filter(lesson_id=rep)
        for que in questions:
            if que in liste_ques:
                pass
            else:
                liste_ques.append(que.id)
            for op in liste_ques:
                opquestion = OptionQuestion.objects.filter(question_id=op)
                for opq in opquestion:
                    if opq.question_id in liste_quesf:
                        pass
                    else:
                        liste_quesf.append(opq.question_id)
    print('liste des question des lesson ', liste_ques)
    print('liste des  question de l evaluation ', liste_quesf)
    print('les lesson', chek)
    b = request.POST['interne']
    if form.is_valid():
        evaluation = form.save(commit=False)
        evaluation.types = "Interrogation"
        if int(b) > 0:
            evaluation.interne = 1
        else:
            evaluation.interne = 0
        evaluation.user_id = auteur.id
        evaluation.typeId = chek
        evaluation.save()
        x = evaluation.id
        for qu in liste_quesf:
            try:
                cur.execute("INSERT INTO oorax_questionevaluation (evaluation_id,question_id)  VALUES (%s,%s) ",
                            [x, qu])
                conn.commit()
            except:
                # Rollback in case there is any error
                conn.rollback()
        return redirect('interrogation', id=a)

    cour = Cour.objects.get(id=id)
    cour_titre = cour.titre
    cour_auteur = cour.auteur
    lesson = Lesson.objects.all()
    chapitre = Chapitre.objects.filter(courid_id=cour.id)
    evalu = Evaluation.objects.all()
    liste_eva = []
    for li in lesson:

        if li.chapitreid_id is chapitre[0].id:
            for ev in evalu:
                if li.id in ev.typeId:
                    evaluation = ev.id
        else:
            pass
    contenu = Contenue.objects.all()
    return render(request, 'registration/contenu_mes_cours.html', {
        'contenu': contenu, 'lesson': lesson,
        'chapitre': chapitre, 'cour_titre': cour_titre,
        'cour_auteur': cour_auteur, 'evaluation': evaluation, })






{% for interro in lesson %}
                                        {% for ev in evalu %}
                                            {% if interro.id in liste_chap %}

                                                <ul>
                                                    {% if interro.id in ev.typeId %}
                                                        <li class="dist">
                                                         <input type="radio"  name="check"  id="checks" value="{{ interro.id }}">{{ interro.nom_lesson }}
                                                        </li>
                                                    {% else %}
                                                        <li>
                                                         <input type="radio"  name="check"  id="check" value="{{ interro.id }}">{{ interro.nom_lesson }}
                                                        </li>
                                                    {% endif %}
                                                 </ul>

                                            {% endif %}
                                        {% endfor %}
                                {% endfor %}
*

cour = Cour.objects.get(id=id)
lessons = Lesson.objects.all()
liste_less = []
cour_id = cour.id
cour_titre = cour.titre
cour_auteur = cour.auteur
evalua = Evaluation.objects.all()
sessevalu = SessionEvaluation.objects.all()
i = 0
n = 0
chapitre = Chapitre.objects.filter(courid_id=cour_id)
while len(chapitre) > 0:
    lesson = Lesson.objects.filter(chapitreid_id=chapitre[0].id)
    while len(lesson) > 0:
        for less in lesson:
            liste_less.append(less.id)
            for evas in evalua:
                for x in evas.typeId:
                    if x is liste_less[0]:
                        for sessa in sessevalu:
                            if sessa.evaluation_id is evas.id:
                                if sessa.point >= 90:
                                    a = evas.id
                                else:
                                    a = sessa.evaluation_id
        n = n + 1

    i = i + 1

for evas in evalua:
    for x in evas.typeId:
        if x is liste_less[0]:
            a = evas.id
        print('montr le a', a)
        print('montr le x', x)

        for evas in evalua:
            for x in evas.typeId:
                print('premier', liste_less[0], 'deuxieme', liste_less[1], x)
                print('mon', i, 'et mon x', x)
                if x is liste_less[i]:
                    print(liste_less[i])
                    a = evas.id
                    i = i + 1
                else:





                        if sess.point>=90:
                            print('vous avez 90 %')
                        else:
                            for x in evas.typeId:
                                if x is liste_less[i]:
                                    print(x,"ok")
                                    a = evas.id
                    else:
                        print("vous n'avez pas encore fait cette evaluation")
                        for x in evas.typeId:
                            if x is liste_less[i]:
                                print(x, "ok")
                                a = evas.id

if sessevalu:
    for sess in sessevalu:
        if evas.id is sess.evaluation_id:
            if sess.point >= 90:
                print('vous avez 90 %')
                # i = i + 1
                for x in evas.typeId:
                    b = i + 1
                    print(x, 'premier', liste_less[b])
                    if x is liste_less[i]:
                        print('deux', b)
                        print('deuxieme', liste_less[b])
                        print(x, "ok")
                        a = evas.id
                        contenu = Contenue.objects.all()
                        return render(request, 'registration/contenu_mes_cours.html',
                                      {'contenu': contenu, 'lesson': lesson,
                                       'chapitre': chapitre, 'cour_titre': cour_titre,
                                       'cour_auteur': cour_auteur, 'a': a})
            else:
                print('vous n avez pas eu 90%')
                for x in evas.typeId:
                    if x is liste_less[i]:
                        print(x, "ok", evas.id)
                        a = evas.id
                        contenu = Contenue.objects.all()
                        return render(request, 'registration/contenu_mes_cours.html',
                                      {'contenu': contenu, 'lesson': lesson,
                                       'chapitre': chapitre, 'cour_titre': cour_titre,
                                       'cour_auteur': cour_auteur, 'a': a})

        else:
            # print('vous n avez pas encore fais levaluation')
            for x in evas.typeId:
                if x is liste_less[i]:
                    print(x, "ok")
                    a = evas.id
                    contenu = Contenue.objects.all()
                    return render(request, 'registration/contenu_mes_cours.html',
                                  {'contenu': contenu, 'lesson': lesson,
                                   'chapitre': chapitre, 'cour_titre': cour_titre,
                                   'cour_auteur': cour_auteur, 'a': a})
else:
    print('rien dans sesseva ')
    for x in evas.typeId:
        if x is liste_less[i]:
            print(x, "ok")
            a = evas.id
            contenu = Contenue.objects.all()
            return render(request, 'registration/contenu_mes_cours.html',
                          {'contenu': contenu, 'lesson': lesson,
                           'chapitre': chapitre, 'cour_titre': cour_titre,
                           'cour_auteur': cour_auteur, 'a': a})

        for x in evas.typeId:
            b = i + 1
            print(x, 'premier', liste_less[b])
            if x is liste_less[i]:
                print('deux', b)
                print('deuxieme', liste_less[b])
                print(x, "ok")
                a = evas.id
                contenu = Contenue.objects.all()
                return render(request, 'registration/contenu_mes_cours.html',
                              {'contenu': contenu, 'lesson': lesson,
                               'chapitre': chapitre, 'cour_titre': cour_titre,
                               'cour_auteur': cour_auteur, 'a': a})














            ## a prendre
            else:
                print('vous n avez pas encore fais levaluation')
                for x in evas.typeId:
                    if x is liste_less[i]:
                        print(x, "ok", i)
                        a = evas.id
                        contenu = Contenue.objects.all()
                        return render(request, 'registration/contenu_mes_cours.html',
                                      {'contenu': contenu, 'lesson': lesson,
                                       'chapitre': chapitre, 'cour_titre': cour_titre,
                                       'cour_auteur': cour_auteur, 'a': a})
            else:
            print('rien dans sesseva ')
            for x in evas.typeId:
                if x is liste_less[i]:
                    print(x, "ok")
                    a = evas.id
                    contenu = Contenue.objects.all()
                    return render(request, 'registration/contenu_mes_cours.html',
                                  {'contenu': contenu, 'lesson': lesson,
                                   'chapitre': chapitre, 'cour_titre': cour_titre,
                                   'cour_auteur': cour_auteur, 'a': a})






                ##nouveaun a prendre
                if poin_lt[0] >= 90:
                    print('vous avez 90 %', evas.id, poin_lt[-1])
                    for x in evas.typeId:
                        if x is liste_less[i - 1]:
                            a = evas.id
                            print(x, 'premier', i, a, liste_less[i - 1])
                            contenu = Contenue.objects.all()
                            return render(request, 'registration/contenu_mes_cours.html',
                                          {'contenu': contenu, 'lesson': lesson,
                                           'chapitre': chapitre, 'cour_titre': cour_titre,
                                           'cour_auteur': cour_auteur, 'a': a})
                else:
                    a = evas.id
                    print('vous n avez pas 90%', a)
                    contenu = Contenue.objects.all()
                    return render(request, 'registration/contenu_mes_cours.html',
                                  {'contenu': contenu, 'lesson': lesson,
                                   'chapitre': chapitre, 'cour_titre': cour_titre,
                                   'cour_auteur': cour_auteur, 'a': a})
