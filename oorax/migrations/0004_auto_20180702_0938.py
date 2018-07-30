# Generated by Django 2.0.6 on 2018-07-02 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oorax', '0003_auto_20180630_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Typetransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle_transaction', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='user_envoi_Id',
            new_name='user_entree',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='user_recu_Id',
            new_name='user_sortie',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='types_user_envoi',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='types_user_recu',
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='oorax.Typetransaction'),
        ),
    ]
