from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from account.forms import AccountRegisterForm
from account.models import AccountGroup, Account, Group
from adminpanel.forms import AdminAccountGroupForm


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAccountGroupForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {"form": form, "adminGroup": adminGroup}
    if adminGroup:
        if form.is_valid():
            userId = form.cleaned_data.get("userId")
            groupId = form.cleaned_data.get("groupId")
            isActive = form.cleaned_data.get("isActive")
            if AccountGroup.objects.filter(Q(groupId=groupId) and Q(userId=userId)):
                messages.error(request, 'Bu kullanıcıya izin daha önce eklenmiş.')
            else:
                instance = AccountGroup(userId=userId, groupId=groupId, isActive=isActive)
                instance.save()
                messages.success(request, "Kullanıcıya başarıyla grup eklendi.")
                return redirect("admin_add_account_group")
        return render(request, "admin/account/add-account-group.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_users(request):
    users = Account.objects.all()
    context = {
        "users": users,
    }
    return render(request, "admin/account/account.html", context)


@login_required(login_url="login_admin")
def admin_account_groups(request):
    accountGroups = AccountGroup.objects.all()
    context = {
        "accountGroups": accountGroups,
    }
    return render(request, "admin/account/account-group.html", context)


@login_required(login_url="login_admin")
def admin_add_account(request):
    form = AccountRegisterForm(request.POST or None)
    getGroup = Group.objects.get(slug="uye")
    accountGroup = AccountGroup()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            new_user = Account(username=username, email=email, first_name=first_name, last_name=last_name)
            new_user.save()
            new_user.set_password(password)
            new_user.save()
            accountGroup.userId_id = new_user.id
            accountGroup.groupId_id = getGroup.id
            accountGroup.save()
            messages.success(request, "Kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("admin_users")
        context = {
            "form": form,
            "adminGroup": adminGroup
        }
        return render(request, "admin/account/new-user.html", context)
    else:
        messages.error(request, "Yetkiniz Yok !")
        return redirect("admin_users")