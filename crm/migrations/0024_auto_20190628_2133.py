# Generated by Django 2.2 on 2019-06-28 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_auto_20190628_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordfirm',
            name='last_visit',
            field=models.DateField(),
        ),
    ]