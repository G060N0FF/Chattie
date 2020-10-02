from django.shortcuts import render
from .forms import GroupNameForm
from django.contrib.auth.decorators import login_required


@login_required
def select_group(request):
    form = GroupNameForm()
    groups = request.user.user_groups.all()

    if request.method == "POST":
        print(1)

    context = {'form': form, 'groups': groups}
    return render(request, 'Group_messages/select_group.html', context)
