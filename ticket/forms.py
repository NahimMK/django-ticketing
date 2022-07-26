from django import forms
from .models import Replie

class ReplieModelForm(forms.ModelForm):
    class Meta:
        model = Replie
        fields = ['ticket', 'body']
        widgets = {
            'ticket': forms.HiddenInput(),
            'body': forms.Textarea(attrs={'placeholder': 'Write your comment here...'}),
        }