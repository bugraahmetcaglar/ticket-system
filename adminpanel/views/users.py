import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from account.forms import AccountRegisterForm
from account.models import AccountGroup, Account, Group
from account.views import current_user_group
from adminpanel.forms import AdminAccountGroupForm
from track.models import Ticket


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAccountGroupForm(request.POST or None)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    context = {
        "form": form,
        "accountGroup": accountGroup,
        "unreadCount": unreadCount,
    }
    if accountGroup:
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
        messages.error(request, "You don't have permission.")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_edit_account(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    instance = Account.objects.get(username=username)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    context = {
        "instance": instance,
        "accountGroup": accountGroup,
        "unreadCount": unreadCount,
    }
    if accountGroup == "chief":
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            instance.username = username
            instance.email = email
            instance.first_name = first_name
            instance.last_name = last_name
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "The user was successfully updated.")
            return render(request, "admin/account/edit-account.html", context)
        return render(request, "admin/account/edit-account.html", context)
    else:
        messages.error(request, "You don't have permission")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_users(request):
    """
    :param request:
    :return:
    """
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    users = Account.objects.all()
    context = {
        "users": users,
        "accountGroup": accountGroup,
        "unreadCount": unreadCount,
    }
    return render(request, "admin/account/account.html", context)


@login_required(login_url="login_admin")
def admin_account_groups(request):
    """
    :param request:
    :return:
    """
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    groups = AccountGroup.objects.all()
    context = {
        "groups": groups,
        "accountGroup": accountGroup,
        "unreadCount": unreadCount,
    }
    return render(request, "admin/account/account-group.html", context)


@login_required(login_url="login_admin")
def admin_add_account(request):
    """
    :param request:
    :return:
    """
    form = AccountRegisterForm(request.POST or None)
    getGroup = Group.objects.get(slug="user")
    group = AccountGroup()
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    accountGroup = current_user_group(request, request.user)
    if accountGroup == "chief":
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
            "unreadCount": unreadCount,
            "accountGroup": accountGroup,
        }
        return render(request, "admin/account/new-user.html", context)
    else:
        messages.error(request, "You don't have permission")
        return redirect("admin_users")


@login_required(login_url="login_admin")
def admin_block_account(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    accountGroup = current_user_group(request, request.user)
    try:
        instance = Account.objects.get(username=username)
        if accountGroup == 'chief':
            if instance.is_active:
                instance.is_active = False
                instance.save()
                return redirect("admin_users")
            else:
                instance.is_active = True
                instance.save()
                return redirect("admin_users")
        else:
            messages.error(request, "You don't have permission")
            return redirect("admin_users")
    except:
        messages.error(request, "User couldn't find")
        return redirect("admin_users")


@login_required(login_url="login_admin")
def admin_add_group_to_user(request):
    """
    :param request:
    :return:
    """
    accountGroup = current_user_group(request, request.user)
    unreadCount = Ticket.objects.filter(isRead=False, isActive=True).count()
    groups = Group.objects.all()
    users = Account.objects.all()
    context = {
        "accountGroup": accountGroup,
        "groups": groups,
        "users": users,
        "unreadCount": unreadCount,
    }
    if accountGroup == "chief":
        if request.method == "POST":
            userId = request.POST['userId']
            groupId = request.POST['groupId']
            try:
                getExistAccount = AccountGroup.objects.get(userId=userId)
                if getExistAccount:
                    getExistAccount.groupId_id = groupId
                    getExistAccount.save()
                    messages.success(request, "Successfully Changed.")
                    return redirect("admin_account_groups")
            except:
                instance = AccountGroup()
                instance.groupId_id = groupId
                instance.userId_id = userId
                instance.save()
                messages.success(request, "Successfully added.")
                return redirect("admin_index")
    else:
        messages.error(request, "You don't have permission.")
        return redirect("admin_users")
    return render(request, "admin/account/group/add-group-to-user.html", context)
