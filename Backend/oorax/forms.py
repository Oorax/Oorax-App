from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    fonction = forms.ModelChoiceField(queryset=Group.objects.filter(Q(id=1) | Q(id=3)))
    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('username', 'email','fonction','contact','image',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','contact','image', 'password',)

class CategorieForm(forms.ModelForm):

     class Meta:
        model = Categorie
        fields = ('nom_categorie',)

class CourForm(forms.ModelForm):
    class Meta:
        model = Cour
        fields = ('titre','description','image',)

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
        fields = ('reference',)

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('montant',)

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ("cour",)

class InscritForm(forms.ModelForm):
    class Meta:
        model = Inscrit
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

class ChapEvaluationForm(forms.ModelForm):
    class Meta:
        model = ChapEvaluation
        fields = ('point',)

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ('description','prix','duree',)


class QuestionEvaluationForm(forms.ModelForm):
    class Meta:
        model = QuestionEvaluation
        fields = ('evaluation',)


class CheckForm(forms.ModelForm):
    class Meta:
        model=Check
        fields = ('check',)

class DomaineForm(forms.ModelForm):
    class Meta:
        model=Domaine
        fields = ('nom_domaine',)

class ActivationListe(forms.ModelForm):
    liste = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(email_validated=0), widget=forms.CheckboxSelectMultiple,)
    class Meta:
        model = CustomUser
        fields = ('liste',)

class BlackListe(forms.ModelForm):
    liste = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(blocker=0), widget=forms.CheckboxSelectMultiple,)
    class Meta:
        model = CustomUser
        fields = ('liste',)


class WhiteListe(forms.ModelForm):
    liste = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(blocker=1), widget=forms.CheckboxSelectMultiple,)
    class Meta:
        model = CustomUser
        fields = ('liste',)





