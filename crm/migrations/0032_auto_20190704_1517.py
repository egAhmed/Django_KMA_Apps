# Generated by Django 2.2.2 on 2019-07-04 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0031_auto_20190702_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='record',
        ),
        migrations.AddField(
            model_name='recordfirm',
            name='client',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='crm.Clients'),
        ),
    ]
