# Generated by Django 3.2.15 on 2023-09-25 19:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
