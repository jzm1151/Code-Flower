# Generated by Django 4.0.2 on 2022-04-15 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_instructorrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructorrequest',
            name='pref_name',
            field=models.CharField(default='temp', max_length=300),
            preserve_default=False,
        ),
    ]
