# Generated by Django 2.2 on 2020-04-18 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0044_auto_20200415_0238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clients',
            old_name='_notes',
            new_name='notes',
        ),
    ]
