from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def sign_up(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('/')
    context = {"form": form}

    return render(request, 'registration/sign_up.html', context)


@login_required
def index(request):
    context = {}
    return render(request, 'Home/index.html', context)
