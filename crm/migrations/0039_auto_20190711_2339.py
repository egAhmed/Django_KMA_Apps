# Generated by Django 2.2.2 on 2019-07-11 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_auto_20190711_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordfirm',
            name='client',
        ),
        migrations.AddField(
            model_name='recordfirm',
            name='client_id',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.SET_DEFAULT, to='crm.Clients'),
        ),
    ]
