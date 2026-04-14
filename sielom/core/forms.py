from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ("name", "email", "phone", "comment", "is_active")