# Generated by Django 2.2.2 on 2019-07-04 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_auto_20190704_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordfirm',
            name='client',
        ),
    ]