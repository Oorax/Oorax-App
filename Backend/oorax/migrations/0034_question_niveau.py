# Generated by Django 2.0.6 on 2018-07-23 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0033_sessionevaluation_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='niveau',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='oorax.Niveau'),
        ),
    ]