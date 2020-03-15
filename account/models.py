import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save

from wwttms.slug import slug_save


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name="Başlık")
    slug = models.SlugField(unique=True, blank=False, null=False, max_length=254, verbose_name="Slug")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Permission"
        ordering = ["-createdDate"]


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Grup Id")
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name="Grup Adı")
    slug = models.SlugField(unique=True, blank=False, null=False, max_length=254, verbose_name="Slug")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "Group"
        ordering = ["-createdDate"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    address = models.CharField(verbose_name="Adres", max_length=254)
    phoneNumber = models.CharField(verbose_name="Telefon Numarası", null=True, blank=True, max_length=13)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=254)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Account"
        ordering = ["-date_joined"]


class AccountPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    userId = models.ForeignKey(Account, verbose_name="Kullanıcı Adı", on_delete=models.SET_NULL, null=True)
    permissionId = models.ForeignKey(Permission, verbose_name="İzin Adı", on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "AccountPermission"
        ordering = ["-createdDate"]


class GroupPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    permissionId = models.ForeignKey(Permission, verbose_name="İzin Adı", on_delete=models.SET_NULL, null=True)
    groupId = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Grup Adı")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.permissionId

    class Meta:
        db_table = "GroupPermission"
        ordering = ["-createdDate"]


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    userId = models.ForeignKey(Account, verbose_name="Kullanıcı Adı", on_delete=models.SET_NULL, null=True)
    groupId = models.ForeignKey(Group, verbose_name="Grup Adı", on_delete=models.SET_NULL, null=True)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Aktiflik")

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "AccountGroup"
        ordering = ["-createdDate"]


class AccountActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    activityCreator = models.CharField(max_length=254, verbose_name="Oluşturan Kişi")
    activityTitle = models.CharField(max_length=254, verbose_name="Başlık")
    activityDescription = models.CharField(max_length=254, verbose_name="Açıklama")
    activityMethod = models.CharField(max_length=254, verbose_name="Method Türü")
    activityCreatedDate = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulduğu Tarih")
    activityUpdatedDate = models.DateTimeField(verbose_name="Son Güncelleme")

    def __str__(self):
        return self.activityCreator

    class Meta:
        db_table = "AccountActivity"
        ordering = ['-activityCreatedDate']


pre_save.connect(slug_save, sender=Group)
pre_save.connect(slug_save, sender=Permission)