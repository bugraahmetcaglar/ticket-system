import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from account.models import Group
from account.views import current_user_group
from adminpanel.forms import AdminAddGroupForm, AdminEditGroupForm
from track.models import Ticket


@login_required(login_url="login_account")
def admin_all_groups(request):
    """
    :param request:
    :return:
    """
    accountGroup = current_user_group(request, request.user)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    if accountGroup == "chief":
        groups = Group.objects.all()
        context = {
            "groups": groups,
            "accountGroup": accountGroup,
            "unreadCount": unreadCount,
        }
        return render(request, "admin/groups/group.html", context)
    else:
        messages.error(request, "You don't have permission")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_add_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAddGroupForm(request.POST or None)
    accountGroup = current_user_group(request, request.user)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    context = {
        "form": form,
        "accountGroup": accountGroup,
        "unreadCount": unreadCount,
    }
    if accountGroup == "chief":
        if form.is_valid():
            title = form.cleaned_data.get("title")
            isActive = form.cleaned_data.get("isActive")
            instance = Group(title=title, isActive=isActive)
            instance.save()
            messages.success(request, "Group successfully created")
            return redirect("admin_all_groups")
        return render(request, "admin/groups/add-group.html", context)
    else:
        messages.error(request, "You don't have permission")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_edit_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    accountGroup = current_user_group(request, request.user)
    unreadCount = Ticket.objects.filter(isRead=False).count()
    try:
        if accountGroup == "chief":
            instance = Group.objects.get(slug=slug)
            form = AdminEditGroupForm(request.POST or None, instance=instance)
            context = {
                "instance": instance,
                "form": form,
                "accountGroup": accountGroup,
                "unreadCount": unreadCount,
            }
            if form.is_valid():
                instance = form.save(commit=False)
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "The group was successfully updated")
                return redirect("admin_all_groups")
            return render(request, "admin/groups/edit-group.html", context)
        else:
            messages.error(request, "You don't have permission.")
            return redirect("admin_index")
    except:
        messages.error(request, "The group can not be found.")
        return redirect("admin_all_groups")


@login_required(login_url="login_admin")
def admin_delete_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    accountGroup = current_user_group(request, request.user)
    try:
        if accountGroup == "chief":
            instance = Group.objects.get(slug=slug)
            instance.isActive = False
            instance.save()
            messages.success(request, "The group was successfully deleted")
            return redirect("admin_all_groups")
        else:
            messages.error(request, "You don't have permission")
            return redirect("admin_index")
    except:
        messages.error(request, "The group can not be found.")
        return redirect("admin_groups")
