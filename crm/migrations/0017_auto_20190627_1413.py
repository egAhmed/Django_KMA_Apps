# Generated by Django 2.2 on 2019-06-27 14:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_auto_20190627_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 27, 14, 13, 37, 860486, tzinfo=utc)),
        ),
    ]