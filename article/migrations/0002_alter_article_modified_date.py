# Generated by Django 3.2.13 on 2022-05-22 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
