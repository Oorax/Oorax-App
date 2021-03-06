# Generated by Django 2.0.6 on 2018-09-04 12:14

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0041_chapevaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapevaluation',
            name='evaluation_id',
            field=django_mysql.models.ListCharField(models.IntegerField(default=None, null=True), default='NULL', max_length=66, size=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapevaluation',
            name='reponse',
            field=django_mysql.models.ListCharField(models.IntegerField(default=None, null=True), default='NULL', max_length=66, size=6),
            preserve_default=False,
        ),
    ]
