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