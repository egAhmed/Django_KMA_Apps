# Generated by Django 2.2 on 2019-05-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_recordfirm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recordfirm',
            old_name='firm_name',
            new_name='Company Name',
        ),
    ]
