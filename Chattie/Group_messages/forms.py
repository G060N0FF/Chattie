from django import forms


class GroupCodeForm(forms.Form):
    code = forms.CharField(max_length=200)
