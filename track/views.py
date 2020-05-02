import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.models import Account
from track.forms import TicketForm
from track.models import Ticket, TicketReply


@login_required(login_url="login_account")
def wwttms_index(request):
    """
    :param request:
    :return:
    """
    form = TicketForm(request.POST or None)
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
            messages.success(request, "The ticket was successfully send. We will return as soon as possible")
            return render(request, "wwttms/index.html", {"form": form})
        else:
            messages.error(request, "The email is not matched in our system")
            return render(request, "wwttms/index.html", {"form": form})
    return render(request, "wwttms/index.html", {"form": form})


@login_required(login_url="login_account")
def my_tickets(request):
    tickets = Ticket.objects.filter(creator=request.user)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "wwttms/tickets/my-tickets.html", {"tickets": tickets, "unreadCount": unreadCount})


@login_required(login_url="login_account")
def my_tickets_detail(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    ticketReply = TicketReply.objects.filter(ticketId__ticketNumber=ticketNumber)
    instance.isRead = True
    instance.save()
    return render(request, "wwttms/tickets/my-ticket-detail.html", {"instance": instance, "unreadCount": unreadCount, "ticketReply": ticketReply})


@login_required(login_url="login_account")
def add_reply(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = TicketReply(content=content, creator=request.user)
        new_comment.ticketId = instance
        new_comment.save()
    return redirect(reverse("my_tickets_detail", kwargs={"ticketNumber": ticketNumber}))


@login_required(login_url="login_admin")
def delete_my_ticket(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    instance.delete()
    messages.success(request, "Your ticket was successfully deleted")
    return redirect("my_tickets")
