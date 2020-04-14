from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.forms import AccountLoginForm
from account.models import AccountGroup, Account
from track.models import Ticket, TicketReply


@login_required(login_url="login_admin")
def admin_index(request):
    """
    :param request:
    :return:
    """
    accountGroup = get_account_group(request, request.user.username)
    if accountGroup == 'user' or accountGroup == None:
        messages.error(request, "You don't have permission")
        return redirect("wwttms_index")
    else:
        unreadCount = Ticket.objects.filter(isRead=False).count()
        return render(request, "admin/index.html", {"unreadCount": unreadCount, "accountGroup": accountGroup})


def login_admin(request):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        form = AccountLoginForm(request.POST or None)
        context = {"form": form}
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            getUser = Account.objects.get(email=email)
            if getUser:
                user = authenticate(username=getUser.username, password=password)
            else:
                messages.error(request, "User not found by given email")
                return render(request, "admin/account/login.html", {"form": form})
            if user is None:
                messages.error(request, "User not found.")
                return render(request, "admin/account/login.html", {"form": form})
            else:
                accountGroup = get_account_group(request, getUser.username)
                if accountGroup != 'user':
                    login(request, user)
                    messages.success(request, "Logged in successful")
                    return redirect("admin_index")
                else:
                    messages.error(request, "You dont have permission.")
                    return redirect("wwttms_index")
        else:
            return render(request, "admin/account/login.html", context)
    else:
        return redirect("wwttms_index")


def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect("login_admin")
    else:
        messages.error(request, "You have to logged in")
        return redirect("login_admin")


@login_required(login_url="login_admin")
def all_tickets(request):
    accountGroup = get_account_group(request, request.user)
    tickets = Ticket.objects.all()
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "admin/tickets/tickets.html", {"tickets": tickets, "unreadCount": unreadCount, "accountGroup": accountGroup})


@login_required(login_url="login_admin")
def unread_tickets(request):
    accountGroup = AccountGroup.objects.filter(
        Q(userId__email=request.user.email, groupId__slug="crew-a") | Q(
            userId__email=request.user.email, groupId__slug="chief"))
    unreadTickets = Ticket.objects.filter(isRead=False)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "admin/tickets/unread-tickets.html",
                  {"unreadTickets": unreadTickets, "unreadCount": unreadCount, "accountGroup": accountGroup})


@login_required(login_url="login_admin")
def admin_ticket_detail(request, ticketNumber):
    accountGroup = AccountGroup.objects.filter(
        Q(userId__email=request.user.email, groupId__slug="crew-a") | Q(
            userId__email=request.user.email, groupId__slug="chief"))
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    ticketReply = TicketReply.objects.filter(ticketId__ticketNumber=ticketNumber)
    instance.isRead = True
    instance.save()
    return render(request, "admin/tickets/ticket-detail.html",
                  {"instance": instance, "unreadCount": unreadCount, "ticketReply": ticketReply, "accountGroup": accountGroup})


@login_required(login_url="login_admin")
def admin_add_reply(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = TicketReply(content=content, creator=request.user)
        new_comment.ticketId = instance
        new_comment.save()
    return redirect(reverse("admin_ticket_detail", kwargs={"ticketNumber": ticketNumber}))


def delete_ticket(request, ticketNumber):
    """
    :param request:
    :param ticketNumber:
    :return:
    """
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    instance.delete()
    return redirect("all_tickets")


def get_account_group(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group