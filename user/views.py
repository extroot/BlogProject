from .forms import LoginUserForm

from django.shortcuts import render, redirect
from django.contrib.auth import login


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = LoginUserForm()

    template_name = 'includes/form.html'
    context = {'form': form}
    return render(request, template_name, context)
