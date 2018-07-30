from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('username', 'email','identifiant','code_secret','contact',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username','identifiant', 'email','contact',)

class CategorieForm(forms.ModelForm):
     class Meta:
        model = Categorie
        fields = ('nom_categorie',)

class CourForm(forms.ModelForm):
    class Meta:
        model = Cour
        fields = ('titre','prix',)

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ('nom_chapitre',)

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('nom_lesson',)

class ContenuForm(forms.ModelForm):
    class Meta:
        model = Contenue
        fields = ('titre','contenu_texte',)

class ContenuLienForm(forms.ModelForm):
    class Meta:
        model = Contenue
        fields = ('url','description',)

class RechargerForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('reference',)

class Recharger2Form(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('reference','libelle')

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('montant',)

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ("cour",)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_texte',)

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ('libelle',)

class OptionQuestionForm(forms.ModelForm):
    #juste = forms.ModelMultipleChoiceField(queryset=Option.objects.filter(juste=0),widget=forms.CheckboxSelectMultiple, )
    class Meta:
        model = OptionQuestion
        fields = ('option',)

class SessionEvaluationForm(forms.ModelForm):
    class Meta:
        model = SessionEvaluation
        fields = ('reponse',)

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ('description','prix','duree',)


class QuestionEvaluationForm(forms.ModelForm):
    class Meta:
        model = QuestionEvaluation
        fields = ('evaluation',)






