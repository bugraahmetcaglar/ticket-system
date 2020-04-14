from django import forms


class AccountRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50, label="Username")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    address = forms.CharField(label="Address")
    phoneNumber = forms.CharField(label="Phone Number")
    password = forms.CharField(min_length=6, max_length=50, label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=50, label="Confirm Password", widget=forms.PasswordInput)

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
            raise forms.ValidationError("Passwords are not matched.")

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
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        values = {
            "email": email,
            "password": password
        }
        return values

