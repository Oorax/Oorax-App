# Generated by Django 2.0.6 on 2018-07-03 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0012_delete_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='libelle',
            field=models.CharField(blank=True, max_length=105, null=True),
        ),
    ]
