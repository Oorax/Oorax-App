# Generated by Django 2.0.6 on 2018-11-21 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0053_chapitre_prix_chapitre'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscription',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
