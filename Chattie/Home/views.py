from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def sign_up(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('/')
    context = {"form": form}

    return render(request, 'registration/sign_up.html', context)
