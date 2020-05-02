from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms

from track.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['message',]
    # message = forms.CharField(widget=CKEditorWidget(), label="Message")