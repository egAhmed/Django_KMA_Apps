# Generated by Django 2.2 on 2019-06-27 13:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_auto_20190626_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2019, 6, 27, 13, 40, 26, 585321, tzinfo=utc)),
        ),
    ]
