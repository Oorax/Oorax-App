from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .forms import SignUpForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'denomination']

admin.site.register(Categorie)
admin.site.register(Contenue)
admin.site.register(CustomUser)
admin.site.register(TypeQuestion)
admin.site.register(Transaction)
admin.site.register(Mobilemoney)
admin.site.register(Question)
admin.site.register(Evaluation)
admin.site.register(Cour)
admin.site.register(Niveau)