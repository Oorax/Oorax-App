from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MatiereForm(forms.ModelForm):
     class Meta:
        model = Matiere
        fields = ('titre_mat','description_mat')


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('titre_sess', 'description_sess')

class UserForm(forms.ModelForm):
    class Meta:
        model = UserEleve
        fields = ('nom_user','description_user','solde',)


