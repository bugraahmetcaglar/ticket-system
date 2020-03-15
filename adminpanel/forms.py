from django import forms
from account.models import Permission, Group, GroupPermission, AccountGroup, AccountPermission, Account


class AdminLoginForm(forms.Form):
    email = forms.EmailField(label="Email Adresi")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        values = {
            "email": email,
            "password": password
        }
        return values


class AdminPermissionForm(forms.Form):
    title = forms.CharField(max_length=None, label="İzin Adı")
    slug = forms.SlugField(max_length=None, label="Slug")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminGroupPermissionForm(forms.Form):
    permissionId = forms.ModelChoiceField(queryset=Account.objects.all(), label="İzin Adı")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountGroupForm(forms.Form):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Kullanıcı Adı")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountPermissionForm(forms.Form):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Kullanıcı Adı")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="İzin Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAddGroupForm(forms.Form):
    title = forms.CharField(required=True, label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminEditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'isActive']