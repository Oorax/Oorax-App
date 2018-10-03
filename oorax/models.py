from datetime import date
from django.utils import  timezone
from django.db.models import CharField, IntegerField
from django_mysql.models import ListCharField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.

class CustomUser(AbstractUser):
    identifiant = models.CharField(max_length=50, blank=True)
    code_secret = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email_validated = models.BooleanField(default=False)
class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=45, blank=True, null=True)
    parent = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return self.nom_categorie

class Cour(models.Model):
    #user = models.ManyToManyField(CustomUser)
    auteur = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name='+', )
    titre = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    objectif= models.CharField(max_length=255, blank=True, null=True)
    prix = models.FloatField(null=True, blank=True, default=None)
    etat_cour = models.BooleanField(default=False)
    image = models.ImageField(upload_to="logo")
    categorieid = models.ForeignKey(Categorie, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

    

class Chapitre(models.Model):
     nom_chapitre = models.CharField(max_length=200, blank=True, null=True)
     ordre = models.IntegerField(blank=True,null=True)
     objectif = models.CharField(max_length=255, blank=True, null=True)
     courid = models.ForeignKey(Cour, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name='+', )

class ChapEvaluation(models.Model):
    point=models.IntegerField(blank=True,null=True)
    chapitreid = models.ForeignKey(Chapitre, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='+', )
    userid = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='+', )
    reponse = ListCharField(
        base_field=IntegerField(default=None, null=True),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )


class Lesson(models.Model):
    nom_lesson = models.CharField(max_length=200, blank=True, null=True)
    objectif = models.CharField(max_length=255, blank=True, null=True)
    chapitreid = models.ForeignKey(Chapitre, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

class Contenue(models.Model):

    titre = models.CharField(max_length=45, blank=True, null=True)
    contenu_texte = models.TextField(blank=True, null=True)
    types = models.CharField(max_length=45, blank=True, null=True)
    url = models.URLField("Lien de cour", blank=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    lessoneid = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

class Mocle(models.Model):
    courid = models.ForeignKey(Cour, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='+', )

class Lien(models.Model):

    lessoneid = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

class Correction(models.Model):
    #user = models.ManyToManyField(CustomUser)
    titre = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    prix = models.FloatField(null=True, blank=True, default=None)
    audiocorige = models.FloatField(null=True, blank=True, default=None)
    corrigelien = models.ForeignKey(Lien, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )
    a_corrigelien = models.ForeignKey(Lien, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name='+', )

class Evaluation(models.Model):
   # user = models.ManyToManyField(CustomUser)
    types = models.CharField(max_length=45, blank=True, null=True)
    duree = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    prix = models.FloatField(null=True, blank=True, default=None)
    interne = models.BooleanField(default=False)
    typeId = ListCharField(
        base_field=IntegerField(default=None, null=True),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                         related_name='+', )
    
class SessionEvaluation(models.Model):
    #reponsse = models.CharField(max_length=20, blank=True, null=True)
    reponse = ListCharField(
        base_field=IntegerField(default=None, null=True),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )
    duree = models.IntegerField(blank=True, null=True)
    point = models.IntegerField(blank=True,null=True)
    date_evaluation = models.DateTimeField(blank=True, default=timezone.now)
    evaluation = ListCharField(
        base_field=IntegerField(default=None, null=True),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='+', )
    userid= models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='+', )

class Mobilemoney(models.Model):
    raisonsocial = models.TextField(blank=True, null=True)
    adresse = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

class Niveau(models.Model):
    libelle = models.CharField(max_length=45,blank=True, null=True)
    code = models.CharField(max_length=45, blank=True, null=True)

class TypeQuestion(models.Model):
    libelle = models.CharField(max_length=45,blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)

class Question(models.Model):
      explication = models.CharField(max_length=455, blank=True, null=True)
      visible=models.BooleanField(default=0)
      niveau = models.ForeignKey(Niveau, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )
      question_texte= models.CharField(max_length=200, blank=True, null=True)
      user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )
      typequestion = models.ForeignKey(TypeQuestion, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='+', )
      lesson = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

class Check(models.Model):
    check = models.BooleanField(default=0)
    temps=models.BooleanField(default=0)


class Option(models.Model):
    libelle = models.CharField(max_length=45, blank=True, null=True)

class OptionQuestion(models.Model):
    juste = models.BooleanField(default=0)
    option=models.ForeignKey(Option, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )
    question=models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

class QuestionEvaluation(models.Model):
     evaluation = models.ForeignKey(Evaluation, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='+', )
     question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='+', )

class Tutorat(models.Model):
    #user = models.ManyToManyField(CustomUser)
    titre = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    prix = models.FloatField(null=True, blank=True, default=None)
    duree = models.IntegerField(blank=True, null=True)

class Typetransaction(models.Model):
    libelle_transaction = models.CharField(max_length=200, blank=True, null=True)

class Transaction(models.Model):
    user_entree = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='+', )

    user_sortie = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='+', )

    #transaction = models.ForeignKey(Typetransaction, blank=True, null=True, on_delete=models.CASCADE,
                                      # related_name='+', )

    mobile_moneyId = models.ForeignKey(Mobilemoney, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name='+', )

    libelle= models.CharField(max_length=45, blank=True, null=True)
    reference = models.CharField(max_length=45, blank=True, null=True)
    montant = models.FloatField(null=True, blank=True, default=None)
    #date_transaction = models.DateTimeField(blank=True, default=timezone.now)
    date_transactions = models.DateTimeField(blank=True, default=timezone.now)

class Inscription(models.Model):
    transaction = models.ForeignKey(Transaction, models.DO_NOTHING)
    cour = models.ForeignKey(Cour, models.DO_NOTHING)

class AchatTutorat(models.Model):
    transaction = models.ForeignKey(Transaction, models.DO_NOTHING)
    tutorat = models.ForeignKey(Tutorat, models.DO_NOTHING)

class AchatEvaluation(models.Model):
    transaction = models.ForeignKey(Transaction, models.DO_NOTHING)
    evaluation = models.ForeignKey(Evaluation, models.DO_NOTHING)


class Annonce(models.Model):
    titre = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)


