from django import forms


class GroupCodeForm(forms.Form):
    code = forms.CharField(max_length=10)


class GroupCreationForm(forms.Form):
    name = forms.CharField(max_length=200)
    

class FindUserForm(forms.Form):
    username = forms.CharField(max_length=200)
