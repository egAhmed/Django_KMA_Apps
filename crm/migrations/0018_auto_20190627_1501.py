# Generated by Django 2.2 on 2019-06-27 15:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_auto_20190627_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 27, 15, 1, 29, 390845, tzinfo=utc)),
        ),
    ]
