# Generated by Django 2.2 on 2019-06-26 19:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20190511_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 26, 19, 5, 41, 78188, tzinfo=utc)),
        ),
    ]