# Generated by Django 2.2 on 2019-06-29 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0029_auto_20190629_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordfirm',
            name='paper',
        ),
    ]
