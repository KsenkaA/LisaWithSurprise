# Generated by Django 2.2 on 2019-04-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_extrainfo_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrainfo',
            name='bought',
            field=models.CharField(default='', max_length=1000),
        ),
    ]