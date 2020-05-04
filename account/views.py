from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from account.forms import AccountLoginForm
from account.models import Account, AccountGroup


def login_account(request):
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

            if getUser and getUser.is_active:
                user = authenticate(username=getUser.username, password=password)
            else:
                messages.error(request, "User not found by given email or the user was blocked")
                return render(request, "wwttms/login.html", {"form": form})
            if user is None:
                messages.error(request, "User not found.")
                return render(request, "wwttms/login.html", {"form": form})
            else:
                login(request, user)
                accountGroup = current_user_group(request, user)
                if accountGroup == "chief":
                    messages.success(request, "Welcome " + request.user.username)
                    return redirect("admin_all_tickets")
                else:
                    messages.success(request, "Logged in successful")
                    return redirect("wwttms_index")
        else:
            return render(request, "wwttms/login.html", context)
    else:
        return redirect("wwttms_index")


@login_required(login_url="login_account")
def logout_account(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful.")
        return redirect("login_account")
    else:
        messages.error(request, "You are not logged in")
        return redirect("login_account")


def current_user_group(self, email):
    """
    :param self:
    :param email:
    :return:
    """
    try:
        group = AccountGroup.objects.get(userId__email=email)
        return str(group.groupId)
    except:
        group = None
        return group