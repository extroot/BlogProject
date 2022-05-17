from .forms import LoginUserForm, CreateUserForm

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


def registration(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.is_active = False
            user = user_form.save()
            # user.is_active = False
            user.save()

            return redirect('/login')
    else:
        user_form = CreateUserForm()

    template_name = 'includes/form.html'
    context = {'form': user_form}
    return render(request, template_name, context)
