from django.contrib.auth.models import User, Group
from rest_framework.serializers import ModelSerializer

from oorax.models import *
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('url', 'username', 'email',)

