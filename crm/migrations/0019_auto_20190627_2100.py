# Generated by Django 2.2 on 2019-06-27 21:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0018_auto_20190627_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 27, 21, 0, 1, 506942, tzinfo=utc)),
        ),
    ]
