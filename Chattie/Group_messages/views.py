from django.shortcuts import render, redirect
from .forms import GroupCodeForm, GroupCreationForm
from .models import Group
from django.contrib.auth.decorators import login_required

import random
import string


def get_random_alphanumeric_string():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for _ in range(10)))
    return result_str


@login_required
def select_group(request):
    join_form = GroupCodeForm()
    creation_form = GroupCreationForm()
    groups = request.user.user_groups.all()

    if request.method == "POST":
        if 'code' in request.POST:
            form = GroupCodeForm(request.POST)
            if form.is_valid():
                code = request.POST['code']
                try:
                    group = Group.objects.get(code=code)
                except:
                    context = {'error': "There is not a group that matches this password"}
                    return render(request, 'Group_messages/error.html', context)
                return redirect('/chat/'+str(group.pk))
        elif 'name' in request.POST:
            form = GroupCreationForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                while True:
                    try:
                        new_group = Group(name=name, code=get_random_alphanumeric_string())
                        new_group.save()
                        new_group.users.add(request.user)
                        new_group.save()
                        break
                    except:
                        print("Trying new code")
                return redirect('/group_messages')


                
    context = {'joinForm': join_form, 'creationForm': creation_form, 'groups': groups}
    return render(request, 'Group_messages/select_group.html', context)


@login_required
def chat(request, id):
    print(id)
