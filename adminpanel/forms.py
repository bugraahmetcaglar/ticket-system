from django import forms
from account.models import Permission, Group, GroupPermission, AccountGroup, AccountPermission, Account


class AdminLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        values = {
            "email": email,
            "password": password
        }
        return values


class AdminPermissionForm(forms.Form):
    title = forms.CharField(max_length=None, label="Permission Name")
    slug = forms.SlugField(max_length=None, label="Slug")
    isActive = forms.BooleanField(required=False, label="Is Active")


class AdminGroupPermissionForm(forms.Form):
    permissionId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Permission Name")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Group Name")
    isActive = forms.BooleanField(required=False, label="Is Active")


class AdminAccountGroupForm(forms.Form):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Username")
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Group Name")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountPermissionForm(forms.Form):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Username")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="Permission Name")
    isActive = forms.BooleanField(required=False, label="Is Active")


class AdminAddGroupForm(forms.Form):
    title = forms.CharField(required=True, label="Title")
    isActive = forms.BooleanField(required=False, label="Is Active")


class AdminEditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'isActive']


class AdminEditAccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ['userId', 'groupId']
