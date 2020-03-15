import datetime
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.forms import AccountRegisterForm, AccountLoginForm
from account.models import Account
from track.forms import TicketForm
from track.models import Ticket


def register_account(request):
    if not request.user.is_authenticated:
        form = AccountRegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            address = form.cleaned_data.get("address")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phoneNumber = form.cleaned_data.get("phoneNumber")
            password = form.cleaned_data.get("password")
            new_user = Account(username=username, email=email, address=address, first_name=first_name,
                               last_name=last_name, phoneNumber=phoneNumber)
            new_user.is_active = True
            new_user.is_superuser = False
            new_user.is_staff = False
            new_user.save()
            new_user.set_password(password)
            new_user.save()
            login_user = authenticate(username=username, password=password)
            login(request, login_user)
            messages.success(request, "Başarıyla kayıt oluşturuldu.")
            return redirect("wwttms_index")
        context = {
            "form": form
        }
        return render(request, "wwttms/register.html", context)
    else:
        messages.error(request, "Zaten giriş yapıldı.")
        return redirect("wwttms_index")


def login_account(request):
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
                messages.error(request, "Girdiğiniz mail adresinde kullanıcı bulunamadı")
                return render(request, "wwttms/login.html", {"form": form})
            if user is None:
                messages.error(request, "Böyle bir kullanıcı bulunamadı.")
                return render(request, "wwttms/login.html", {"form": form})
            else:
                login(request, user)
                messages.success(request, "Başarıyla giriş yaptınız")
                return redirect("wwttms_index")
        else:
            return render(request, "wwttms/login.html", context)
    else:
        return redirect("wwttms_index")


def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yaptınız.")
        return redirect("login_account")
    else:
        messages.error(request, "Önce giriş yapmalısınız")
        return redirect("login_account")


