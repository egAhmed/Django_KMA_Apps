# Generated by Django 2.2 on 2020-05-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundrybill',
            name='paidDone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='laundrybill',
            name='returns',
            field=models.BooleanField(default=False),
        ),
    ]
