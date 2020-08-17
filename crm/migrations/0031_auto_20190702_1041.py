# Generated by Django 2.2.2 on 2019-07-02 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0030_remove_recordfirm_paper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.RecordFirm')),
            ],
        ),
        migrations.DeleteModel(
            name='Choices',
        ),
    ]
