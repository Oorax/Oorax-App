# Generated by Django 2.0.6 on 2018-11-03 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0049_domaine'),
    ]

    operations = [
        migrations.AddField(
            model_name='cour',
            name='domaineid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='oorax.Domaine'),
        ),
    ]
