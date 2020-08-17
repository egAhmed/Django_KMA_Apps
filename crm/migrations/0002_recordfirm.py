# Generated by Django 2.2 on 2019-05-11 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordFirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(blank=True, max_length=200, null=True)),
                ('manager', models.CharField(blank=True, max_length=200, null=True)),
                ('repres_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_visit', models.DateField()),
                ('notes', models.TextField()),
            ],
        ),
    ]