# Generated by Django 2.0.6 on 2018-07-05 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0015_auto_20180705_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_texte',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='duree',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
