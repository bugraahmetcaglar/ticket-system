from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from account.forms import AccountLoginForm
from account.models import AccountGroup
from adminpanel.forms import AdminLoginForm


@login_required(login_url="login_admin")
def admin_index(request):
    """
    :param request:
    :return:
    """
    return render(request, "admin/index.html")


def login_admin(request):
    if request.user.is_authenticated:
        messages.error(request, "Zaten Giriş Yapılmış")
        return redirect("admin_index")
    else:
        form = AdminLoginForm(request.POST or None)
        context = {"form": form}
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            accountGroup = AccountGroup.objects.filter(
                Q(userId__username=form.cleaned_data.get('username'), groupId__slug="moderator") | Q(
                    userId__username=form.cleaned_data.get('username'), groupId__slug="admin"))
            if accountGroup:
                user = authenticate(username=username, password=password)
                if user is None:
                    return render(request, "admin/account/login.html", {"form": form, "accountGroup": accountGroup})
                else:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "Hoş geldiniz " + user.get_full_name())
                        return redirect("admin_index")
                    else:
                        messages.error(request, "Kullanıcı aktif değil !")
                        return redirect("login_admin")
            else:
                messages.error(request,
                               "Admin paneline giriş yetkiniz yok ya da böyle bir kullanıcı bulunamadı.")
                return redirect("login_admin")
    return render(request, "admin/account/login.html", context)


def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yaptınız.")
        return redirect("login_admin")
    else:
        messages.error(request, "Önce giriş yapmalısınız")
        return redirect("login_admin")