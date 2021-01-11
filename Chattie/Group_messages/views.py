from django.shortcuts import render, redirect
from .forms import GroupCodeForm, GroupCreationForm, FindUserForm
from .models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator

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
                if request.user not in group.users.all():
                    group.users.add(request.user)
                    group.save()
                else:
                    context = {'error': "You are already a member of this group"}
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
    group = Group.objects.get(pk=id)
    username = request.user.username
    if request.user not in group.users.all():
        context = {'error': "You are not a member of this group"} 
        return render(request, 'Group_messages/error.html', context)

    context = {'group': group, "room_name": id, 'username': username}
    return render(request, 'Group_messages/chat.html', context)
    
    
@login_required
def settings(request, id):
    group = Group.objects.get(pk=id)
    name_form = GroupCreationForm()
    find_user_form = FindUserForm()
    username = request.user.username
    users = []
    
    if request.user not in group.users.all():
        context = {'error': "You are not a member of this group"} 
        return render(request, 'Group_messages/error.html', context)
        
    if request.method == "POST":
        if "name" in request.POST:
            name_form = GroupCreationForm(request.POST)
            if name_form.is_valid():
                group.name = request.POST['name']
                group.save()
                return redirect('/group_messages/chat/'+str(id))
        elif "username" in request.POST:
            find_user_form = FindUserForm(request.POST)
            if find_user_form.is_valid():
                users = User.objects.filter(username__icontains=request.POST['username'])
                context = {
                    'group': group,
                    'name_form': name_form,
                    'find_user_form': find_user_form,
                    'users': users,
                    'username': username
                }
                return render(request, 'Group_messages/settings.html', context)

    context = {
        'group': group,
        'name_form': name_form,
        'find_user_form': find_user_form,
        'users': users,
        'username': username
    }
    return render(request, 'Group_messages/settings.html', context)
    

@login_required
def add(request, group_id, user_id):
    group = Group.objects.get(pk=group_id)
    user = User.objects.get(pk=user_id)
    
    if request.user not in group.users.all():
        error = "You are not a member of the group you are trying to add members to"
        context = {'error': error}
        return render(request, 'Group_messages/error.html', context)
    
    if user in group.users.all():
        error = "This user is already a member of the group"
        context = {'error': error}
        return render(request, 'Group_messages/error.html', context)
        
    group.users.add(user)
    group.save()
    return redirect('/group_messages/settings/' + str(group_id))


@login_required
def remove(request, group_id, user_id):
    group = Group.objects.get(pk=group_id)
    user = User.objects.get(pk=user_id)

    if request.user not in group.users.all():
        error = "You are not a member of the group you are trying to remove members from"
        context = {'error': error}
        return render(request, 'Group_messages/error.html', context)

    if user not in group.users.all():
        error = "This user is not a member of the group"
        context = {'error': error}
        return render(request, 'Group_messages/error.html', context)

    group.users.remove(user)
    group.save()
    if user == request.user:
        return redirect('/group_messages/')
    else:
        return redirect('/group_messages/chat/'+str(group_id))


@login_required
def load_messages(request):
    room_id = request.GET.get("roomName")
    group = Group.objects.get(pk=room_id)
    messages = group.messages.order_by('date')
    messages_paged = Paginator(messages, 20)
    current_page = int(request.GET.get("page"))
    messages = messages_paged.page(messages_paged.num_pages - current_page)
    data = {}
    all_messages = []
    for message in messages[::-1]:
        all_messages.append([message.user.username, message.text])
    data['messages'] = all_messages
    return JsonResponse(data)
