# Generated by Django 2.0.6 on 2018-07-09 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0019_transaction_date_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='date_transaction',
        ),
    ]
