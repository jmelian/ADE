# Generated by Django 2.1.3 on 2018-11-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('reglas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reglas',
            name='persona',
        ),
        migrations.RemoveField(
            model_name='reglas',
            name='vacuna',
        ),
        migrations.AddField(
            model_name='reglas',
            name='usuario',
            field=models.ManyToManyField(blank=True, null=True, to='usuarios.Usuarios'),
        ),
        migrations.DeleteModel(
            name='Vacuna',
        ),
    ]
