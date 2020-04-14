from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from account.forms import AccountRegisterForm, AccountLoginForm
from account.models import Account, AccountGroup, Group


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
            getGroup = Group.objects.get(slug="user")
            new_group = AccountGroup(userId=new_user, groupId=getGroup)
            new_group.save()
            login_user = authenticate(username=username, password=password)
            login(request, login_user)
            messages.success(request, "Registration successfully created.")
            return redirect("wwttms_index")
        context = {
            "form": form
        }
        return render(request, "wwttms/register.html", context)
    else:
        messages.error(request, "You already logged in.")
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
                messages.error(request, "User not found by given email")
                return render(request, "wwttms/login.html", {"form": form})
            if user is None:
                messages.error(request, "User not found.")
                return render(request, "wwttms/login.html", {"form": form})
            else:
                login(request, user)
                messages.success(request, "Logged in successful")
                return redirect("wwttms_index")
        else:
            return render(request, "wwttms/login.html", context)
    else:
        return redirect("wwttms_index")


def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect("login_account")
    else:
        messages.error(request, "You are not logged in")
        return redirect("login_account")


def current_user_group(self, username):
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group
