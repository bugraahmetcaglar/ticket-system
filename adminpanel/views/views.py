from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.forms import AccountLoginForm
from account.models import AccountGroup, Account
from adminpanel.forms import AdminLoginForm
from track.models import Ticket, TicketReply


@login_required(login_url="login_admin")
def admin_index(request):
    """
    :param request:
    :return:
    """
    # accountGroup = AccountGroup.objects.filter(
    #     Q(userId__username=request.user.username, groupId__slug="moderator") | Q(
    #         userId__username=request.user.username, groupId__slug="chief"))
    # if accountGroup:
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "admin/index.html", {"unreadCount": unreadCount})
    # else:
    #     messages.error(request, "Admin değilsiniz")
    #     return redirect("wwttms_index")


def login_admin(request):
    if not request.user.is_authenticated:
        form = AdminLoginForm(request.POST or None)
        context = {"form": form}
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "Böyle bir kullanıcı bulunamadı.")
                return render(request, "admin/account/login.html", {"form": form})
            else:
                login(request, user)
                messages.success(request, "Başarıyla giriş yaptınız")
                return redirect("admin_index")
        else:
            return render(request, "admin/account/login.html", context)
    else:
        return redirect("admin_index")


# def login_admin(request):
#     if request.user.is_authenticated:
#         messages.error(request, "Zaten Giriş Yapılmış")
#         return redirect("admin_index")
#     else:
#         form = AdminLoginForm(request.POST or None)
#         context = {"form": form}
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             accountGroup = AccountGroup.objects.filter(
#                 Q(userId__email=form.cleaned_data.get('email'), groupId__slug="moderator") | Q(
#                     userId__email=form.cleaned_data.get('email'), groupId__slug="chief"))
#             if accountGroup:
#                 user = authenticate(email=email, password=password)
#                 if user is None:
#                     return render(request, "admin/account/login.html", {"form": form, "accountGroup": accountGroup})
#                 else:
#                     if user.is_active:
#                         login(request, user)
#                         messages.success(request, "Hoş geldiniz " + user.get_full_name())
#                         return redirect("admin_index")
#                     else:
#                         messages.error(request, "Kullanıcı aktif değil !")
#                         return redirect("login_admin")
#             else:
#                 messages.error(request,
#                                "Admin paneline giriş yetkiniz yok ya da böyle bir kullanıcı bulunamadı.")
#                 return redirect("login_admin")
#     return render(request, "admin/account/login.html", context)


def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yaptınız.")
        return redirect("login_admin")
    else:
        messages.error(request, "Önce giriş yapmalısınız")
        return redirect("login_admin")


@login_required(login_url="login_admin")
def all_tickets(request):
    tickets = Ticket.objects.all()
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "admin/tickets/tickets.html", {"tickets": tickets, "unreadCount": unreadCount})


@login_required(login_url="login_admin")
def unread_tickets(request):
    unreadTickets = Ticket.objects.filter(isRead=False)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    return render(request, "admin/tickets/unread-tickets.html", {"unreadTickets": unreadTickets, "unreadCount": unreadCount})


@login_required(login_url="login_admin")
def ticket_detail(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    ticketReply = TicketReply.objects.filter(ticketId__ticketNumber=ticketNumber)
    instance.isRead = True
    instance.save()
    return render(request, "admin/tickets/ticket-detail.html", {"instance": instance, "unreadCount": unreadCount, "ticketReply": ticketReply})


@login_required(login_url="login_admin")
def add_reply(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = TicketReply(content=content, creator=request.user)
        new_comment.ticketId = instance
        new_comment.save()
    return redirect(reverse("ticket_detail", kwargs={"ticketNumber": ticketNumber}))


def delete_ticket(request, ticketNumber):
    instance = get_object_or_404(Ticket, ticketNumber=ticketNumber)
    instance.delete()
    return redirect("all_tickets")