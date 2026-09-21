from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    nome = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("nome",)