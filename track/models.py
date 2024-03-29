import uuid

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import Account, Group


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="creator")
    message = RichTextField()
    first_name = models.CharField(verbose_name="Ad", max_length=254)
    last_name = models.CharField(verbose_name="Soyad", max_length=254)
    email = models.EmailField(verbose_name="Email")
    createdDate = models.DateTimeField(verbose_name="Oluşturulduğu Tarih")
    updatedDate = models.DateTimeField(verbose_name="Son Güncelleme")
    ticketNumber = models.PositiveIntegerField(unique=True, auto_created=True, verbose_name="Ticket Numarası")
    isActive = models.BooleanField(null=True, blank=True, default=True, verbose_name="Aktiflik")
    isRead = models.BooleanField(blank=True, null=True, verbose_name="Okunma", default=False)
    resolved = models.BooleanField(blank=True, null=True, verbose_name="Çözüldü", default=False)
    tree = ArrayField(JSONField(default=dict), blank=True, null=True)
    isTicket = models.BooleanField(default=True, verbose_name="Ticket mı?")
    isReply = models.BooleanField(default=True, verbose_name="Yanıt mı?")
    owner = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")

    def __str__(self):
        return self.ticketNumber

    def save(self, *args, **kwargs):
        if not self.id:
            self.createdDate = timezone.now()

    class Meta:
        db_table = "Ticket"
        ordering = ['-createdDate']

    def __unicode__(self):
        return self.ticketNumber

    def get_absolute_url(self):
        return reverse("ticker_detail", kwargs={"ticketNumber": self.ticketNumber})

    def get_api_url(self):
        return reverse("ticket-api-detail", kwargs={"ticketNumber": self.ticketNumber})

    def children(self):
        return TicketReply.objects.filter(ticketId=self)

    @property
    def any_children(self):
        return TicketReply.objects.filter(ticketId=self.ticketNumber)


class TicketReply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Yorum Id")
    ticketId = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, verbose_name="Ticket Id")
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.SET_NULL, verbose_name="Creator", null=True, blank=True)
    content = RichTextField(verbose_name="Content", blank=False, null=False)
    createdDate = models.DateTimeField(verbose_name="Created Date")
    updatedDate = models.DateTimeField(null=True, blank=True, verbose_name="Updated Date")
    like = models.PositiveIntegerField(default=0, verbose_name="Like")
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.creator

    def save(self, *args, **kwargs):
        if not self.id:
            self.createdDate = timezone.now()

    class Meta:
        db_table = "TicketReply"
        ordering = ['-createdDate']

    def children(self):
        return TicketReply.objects.filter(parentId=self)

    @property
    def any_children(self):
        return TicketReply.objects.filter(parentId=self).exist()