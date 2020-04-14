from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from account.forms import AccountRegisterForm
from account.models import AccountGroup, Account, Group
from account.views import current_user_group
from adminpanel.forms import AdminAccountGroupForm


def admin_add_account_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAccountGroupForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="chief")
    context = {"form": form, "adminGroup": adminGroup}
    if adminGroup:
        if form.is_valid():
            userId = form.cleaned_data.get("userId")
            groupId = form.cleaned_data.get("groupId")
            if AccountGroup.objects.filter(Q(groupId=groupId) and Q(userId=userId)):
                messages.error(request, 'This user has already have a group.')
            else:
                instance = AccountGroup(userId=userId, groupId=groupId)
                instance.save()
                messages.success(request, "Group was added to user successfully.")
                return redirect("admin_add_account_group")
        return render(request, "admin/account/add-account-group.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_users(request):
    currentUser = request.user
    accountGroup = current_user_group(request, currentUser)
    users = Account.objects.all()
    context = {
        "users": users,
        "accountGroup": accountGroup,
    }
    return render(request, "admin/account/account.html", context)


@login_required(login_url="login_admin")
def admin_account_groups(request):
    currentUser = request.user
    accountGroup = current_user_group(request, currentUser)
    groups = AccountGroup.objects.all()
    context = {
        "groups": groups,
        "accountGroup": accountGroup,
    }
    return render(request, "admin/account/account-group.html", context)


@login_required(login_url="login_admin")
def admin_add_account(request):
    form = AccountRegisterForm(request.POST or None)
    currentUser = request.user
    accountGroup = current_user_group(request, currentUser)
    getGroup = Group.objects.get(slug="user")
    group = AccountGroup()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="chief")
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
            group.userId_id = new_user.id
            group.groupId_id = getGroup.id
            group.save()
            messages.success(request, "Registration successfully created.")
            return redirect("admin_users")
        context = {
            "form": form,
            "adminGroup": adminGroup,
            "accountGroup": accountGroup
        }
        return render(request, "admin/account/new-user.html", context)
    else:
        messages.error(request, "You don't have permission")
        return redirect("admin_users")


@login_required(login_url="login_admin")
def block_account(request, username):
    currentUser = request.user
    accountGroup = current_user_group(request, currentUser)
    try:
        instance = Account.objects.get(username=username)
        if accountGroup == 'admin':
            if instance.is_active:
                instance.is_active = False
                instance.save()
                return redirect("all_users")
            else:
                instance.is_active = True
                instance.save()
                return redirect("all_users")
        else:
            messages.error(request, "You don't have permission")
            return redirect("all_users")
    except:
        messages.error(request, "User couldn't find")
        return redirect("all_users")
