import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.views import current_user_group
from track.forms import TicketForm
from track.models import Ticket, TicketReply


@login_required(login_url="login_account")
def wwttms_index(request):
    """
    :param request:
    :return:
    """
    form = TicketForm(request.POST or None)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        matchedEmail = Account.objects.filter(email=email)
        if matchedEmail:
            if form.is_valid():
                message = request.POST.get("message")
            instance = Ticket(first_name=first_name, last_name=last_name, email=email, message=message)
            instance.creator = request.user
            instance.isTicket = True
            rnd = random.randrange(1, 23143215)
            if instance.ticketNumber != rnd:
                instance.ticketNumber = rnd
            else:
                rnd = random.randrange(1, 23143215)
                instance.ticketNumber = rnd
            instance.updatedDate = datetime.datetime.now()
            instance.isActive = True
            instance.isRead = False
            instance.isReply = False
            instance.save()
            instance.parentId_id = instance.id
            instance.save()
            messages.success(request, "The ticket was successfully send. We will return as soon as possible")
            return render(request, "wwttms/index.html", {"form": form, "unreadCount": unreadCount, "accountGroup": accountGroup})
        else:
            messages.error(request, "The email is not matched in our system")
            return render(request, "wwttms/index.html", {"form": form, "unreadCount": unreadCount, "accountGroup": accountGroup})
    return render(request, "wwttms/index.html", {"form": form, "unreadCount": unreadCount, "accountGroup": accountGroup})


@login_required(login_url="login_account")
def my_tickets(request):
    """
    :param request:
    :return:
    """
    tickets = Ticket.objects.filter(creator=request.user, isActive=True)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    return render(request, "wwttms/tickets/my-tickets.html", {"tickets": tickets, "unreadCount": unreadCount, "accountGroup": accountGroup})


@login_required(login_url="login_account")
def my_tickets_detail(request, ticketNumber):
    """
    :param request:
    :param ticketNumber:
    :return:
    """
    instance = Ticket.objects.get(ticketNumber=ticketNumber)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    ticketReply = TicketReply.objects.filter(ticketId__ticketNumber=ticketNumber)
    instance.isRead = True
    instance.save()
    return render(request, "wwttms/tickets/my-ticket-detail.html", {"instance": instance, "unreadCount": unreadCount, "ticketReply": ticketReply, "accountGroup": accountGroup})


@login_required(login_url="login_account")
def add_reply(request, ticketNumber):
    """
    :param request:
    :param ticketNumber:
    :return:
    """
    instance = Ticket.objects.get(ticketNumber=ticketNumber)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    accountGroup = current_user_group(request, request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = TicketReply(content=content, creator=request.user)
        new_comment.ticketId = instance
        new_comment.save()
        messages.success(request, "Successfully replied.")
        return redirect(reverse("my_tickets_detail", kwargs={"ticketNumber": ticketNumber}))
    return render(request, "wwttms/tickets/my-ticket-detail.html", context={"instance": instance, "unreadCount": unreadCount, "accountGroup": accountGroup})


@login_required(login_url="login_admin")
def delete_my_ticket(request, ticketNumber):
    """
    :param request:
    :param ticketNumber:
    :return:
    """
    instance = Ticket.objects.get(ticketNumber=ticketNumber)
    if instance.isActive:
        instance.isActive = False
        messages.success(request, "Your ticket was successfully deleted")
        return redirect("my_tickets")
