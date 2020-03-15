from django import forms

from account.models import Account


class AccountRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50, label="Kullanıcı Adı")
    email = forms.EmailField(label="Email Adresi")
    first_name = forms.CharField(label="Ad")
    last_name = forms.CharField(label="Soyad")
    address = forms.CharField(label="Adres")
    phoneNumber = forms.CharField(label="Telefon Numarası")
    password = forms.CharField(min_length=6, max_length=50, label="Şifre", widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=50, label="Şifre Tekrar", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        address = self.cleaned_data.get("address")
        phoneNumber = self.cleaned_data.get("phoneNumber")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Girilen şifreler uyuşmuyor! Lütfen tekrar deneyin.")

        values = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "password": password,
            "phoneNumber": phoneNumber,
        }
        return values


class AccountLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        values = {
            "email": email,
            "password": password
        }
        return values

