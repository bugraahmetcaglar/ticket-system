# Generated by Django 3.0.2 on 2020-05-29 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0005_remove_ticket_parentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='createdDate',
            field=models.DateTimeField(verbose_name='Oluşturulduğu Tarih'),
        ),
        migrations.AlterField(
            model_name='ticketreply',
            name='createdDate',
            field=models.DateTimeField(verbose_name='Created Date'),
        ),
    ]