# Generated by Django 2.2 on 2019-06-26 21:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20190626_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 26, 21, 29, 49, 381692, tzinfo=utc)),
        ),
    ]
