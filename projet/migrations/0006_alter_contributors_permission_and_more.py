# Generated by Django 4.0.3 on 2022-03-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0005_alter_contributors_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='permission',
            field=models.CharField(choices=[('restricted', 'restricted'), ('all', 'all')], default='all', max_length=20),
        ),
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(choices=[('auteur', 'auteur'), ('contributeur', 'contributeur')], default='auteur', max_length=20),
        ),
    ]
