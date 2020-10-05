from django.shortcuts import render, redirect
from .forms import GroupCodeForm
from .models import Group
from django.contrib.auth.decorators import login_required


@login_required
def select_group(request):
    form = GroupCodeForm()
    groups = request.user.user_groups.all()

    if request.method == "POST":
        form = GroupCodeForm(request.POST)
        if form.is_valid():
            code = request.POST['code']
            try:
                group = Group.objects.get(code=code)
            except:
                return redirect('/group_messages')
            return redirect('/chat/'+str(group.pk))
                
    context = {'form': form, 'groups': groups}
    return render(request, 'Group_messages/select_group.html', context)


@login_required
def chat(request):
    print(1)
