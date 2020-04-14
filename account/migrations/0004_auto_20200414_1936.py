# Generated by Django 3.0.2 on 2020-04-14 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200413_1607'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AccountActivity',
        ),
        migrations.AlterField(
            model_name='account',
            name='address',
            field=models.CharField(max_length=254, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='account',
            name='updatedDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='accountgroup',
            name='groupId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Group', verbose_name='Group Name'),
        ),
        migrations.AlterField(
            model_name='accountgroup',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='accountpermission',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='accountpermission',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='accountpermission',
            name='permissionId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Permission', verbose_name='Permission Name'),
        ),
        migrations.AlterField(
            model_name='accountpermission',
            name='updatedDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='accountpermission',
            name='userId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='group',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='group',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Grup Name'),
        ),
        migrations.AlterField(
            model_name='group',
            name='updatedDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='groupId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Group', verbose_name='Group Name'),
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='isActive',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='permissionId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Permission', verbose_name='Permission Name'),
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='updatedDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Update'),
        ),
    ]
