from django.db import models
from django.contrib.auth.models import AbstractUser



class Session(models.Model):
    titre_sess = models.CharField(max_length=45, blank=True, null=True)
    description_sess = models.CharField(max_length=200, blank=True, null=True)
    prix_sess = models.FloatField(null=True, blank=True, default=None)



class Matiere(models.Model):
    titre_mat = models.CharField(max_length=45, blank=True, null=True)
    description_mat = models.CharField(max_length=200, blank=True, null=True)
    session_mat = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='+', )


class UniteEnseign(models.Model):
    titre_ue = models.CharField(max_length=45, blank=True, null=True)
    description_ue = models.CharField(max_length=200, blank=True, null=True)
    matiere_ue = models.ForeignKey(Matiere, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='+', )

class Programme(models.Model):
    titre_pro = models.CharField(max_length=45, blank=True, null=True)
    description_pro = models.CharField(max_length=200, blank=True, null=True)
    unite_pro = models.ForeignKey(UniteEnseign, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name='+', )

class Centre(models.Model):
    nom_cnt = models.CharField(max_length=45, blank=True, null=True)
    description_cnt = models.CharField(max_length=200, blank=True, null=True)
    session_cnt = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='+', )

class UserEleve(models.Model):
    nom_user = models.CharField(max_length=45, blank=True, null=True)
    description_user= models.CharField(max_length=200, blank=True, null=True)
    solde = models.FloatField(null=True, blank=True, default=None)
    session_user = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='+', )


