# Generated by Django 3.0.2 on 2020-04-13 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200315_1720'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountgroup',
            options={},
        ),
        migrations.RemoveField(
            model_name='accountgroup',
            name='createdDate',
        ),
        migrations.RemoveField(
            model_name='accountgroup',
            name='isActive',
        ),
        migrations.RemoveField(
            model_name='accountgroup',
            name='updatedDate',
        ),
    ]
