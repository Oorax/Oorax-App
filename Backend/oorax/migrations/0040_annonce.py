# Generated by Django 2.0.6 on 2018-08-24 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0039_cour_auteur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
