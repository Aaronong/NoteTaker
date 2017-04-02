from django import forms
from .models import TextEditor


class TextForm(forms.ModelForm):
    class Meta:
        model = TextEditor
        fields = '__all__'


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)