# Generated by Django 2.0.6 on 2018-11-27 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0056_auto_20181127_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargementOmoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('num_transfert', models.CharField(blank=True, max_length=200, null=True)),
                ('montant', models.FloatField(blank=True, default=None, null=True)),
                ('utilise', models.BooleanField(default=0)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
