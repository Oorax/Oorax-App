# Generated by Django 2.0.6 on 2018-07-02 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0004_auto_20180702_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='identServiceId',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='serviceId',
        ),
    ]
