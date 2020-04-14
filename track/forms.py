from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms


class TicketForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=CKEditorWidget(), label="Message")

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        message = self.cleaned_data.get("message")

        values = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "message": message
        }
        return values