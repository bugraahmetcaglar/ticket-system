from django import forms
from account.models import Permission, Group, GroupPermission, AccountGroup, AccountPermission, Account


class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())


class AdminPermissionForm(forms.ModelForm):
    title = forms.CharField(max_length=None, label="İzin Adı")
    slug = forms.SlugField(max_length=None, label="Slug")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminGroupForm(forms.ModelForm):
    title = forms.CharField(max_length=None, label="Grup Adı")
    slug = forms.SlugField(max_length=None, label="Slug")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminGroupPermissionForm(forms.ModelForm):
    permissionId = forms.ModelChoiceField(queryset=Account.objects.all(), label="İzin Adı")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountGroupForm(forms.ModelForm):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Kullanıcı Adı")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountPermissionForm(forms.ModelForm):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Kullanıcı Adı")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="İzin Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")