import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from wwttms.slug import slug_save


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Grup Id")
    title = models.CharField(null=False, blank=False, max_length=100, verbose_name="Grup Name")
    slug = models.SlugField(unique=True, blank=False, null=False, max_length=254, verbose_name="Slug")
    createdDate = models.DateTimeField(verbose_name="Created Date")
    updatedDate = models.DateTimeField(verbose_name="Last Updated", null=True, blank=True)
    isActive = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.createdDate = timezone.now()

    class Meta:
        db_table = "Group"
        ordering = ["-createdDate"]


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updatedDate = models.DateTimeField(verbose_name="Last Updated", null=True, blank=True)
    address = models.CharField(verbose_name="Address", max_length=254)
    phoneNumber = models.CharField(verbose_name="Phone Number", null=True, blank=True, max_length=13)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=254)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Account"
        ordering = ["-date_joined"]


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    userId = models.ForeignKey(Account, verbose_name="Username", on_delete=models.SET_NULL, null=True)
    groupId = models.ForeignKey(Group, verbose_name="Group Name", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "AccountGroup"


pre_save.connect(slug_save, sender=Group)