# Generated by Django 3.2.4 on 2021-07-20 19:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20210719_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='response_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='requestedservice',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 20, 19, 38, 1, 81680, tzinfo=utc), verbose_name='Created on'),
        ),
    ]
