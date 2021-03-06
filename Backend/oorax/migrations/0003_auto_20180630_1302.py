# Generated by Django 2.0.6 on 2018-06-30 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0002_auto_20180629_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='types',
            new_name='types_user_envoi',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='userId',
            new_name='user_envoi_Id',
        ),
        migrations.AddField(
            model_name='transaction',
            name='types_user_recu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user_recu_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
