# Generated by Django 3.1.4 on 2020-12-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]