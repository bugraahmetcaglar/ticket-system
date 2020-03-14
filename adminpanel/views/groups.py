import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from account.models import Group
from adminpanel.forms import AdminAddGroupForm, AdminEditGroupForm


def groups_index(request):
    groups = Group.objects.all()
    context = {
        "groups": groups
    }
    return render(request, "admin/groups/group.html", context)


def add_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAddGroupForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        title = form.cleaned_data.get("title")
        isActive = form.cleaned_data.get("isActive")
        instance = Group(title=title, isActive=isActive)
        instance.save()
        messages.success(request, "Grup başarıyla oluşturuldu")
        return redirect("groups_index")
    return render(request, "admin/groups/add-group.html", context)


@login_required(login_url="login_admin")
def edit_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    form = AdminEditGroupForm(request.POST or None, instance=instance)
    context = {
        "instance": instance,
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Grup başarıyla güncellendi")
        return redirect("groups_index")
    return render(request, "admin/groups/edit-group.html", context)


def delete_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    instance.delete()
    messages.success(request, "Grup başarıyla silindi")
    return redirect("groups_index")
