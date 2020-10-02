from django import forms


class GroupNameForm(forms.Form):
    name = forms.CharField(max_length=200)
