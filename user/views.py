from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import LoginUserForm, CreateUserForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .models import CustomUser
from .utils import send_email_token, token_generator


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                # TODO: отсылать повторно ссылку на почту
                return redirect('home_page')
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
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            email_subject = 'Подтверждение почты'
            email_body = 'Привет, {}, для активации аккаунта перейди по ссылке:\n{}'
            send_email_token(
                user,
                domain,
                url_part='activate',
                email_subject=email_subject,
                email_body=email_body
            )
            # TODO: Сообщение про письмо
            return redirect('/login')
    else:
        user_form = CreateUserForm()

    template_name = 'includes/form.html'
    context = {'form': user_form}
    return render(request, template_name, context)


def logout_page(request):
    logout(request)
    return redirect('home_page')


def verification_email(request, user_id, token):
    if request.user.is_authenticated:
        # TODO: Сообщение, что вход уже выполнен
        return redirect(f'/profile')
    try:
        username = force_str(urlsafe_base64_decode(user_id))
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # TODO: сообщение "что-то пошло не так :)"
        return redirect('/login')

    if user.is_active:
        # TODO: сообщение, что аккаунт уже активен
        return redirect('/login')
    if token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # TODO: сообщение об успехе
        return redirect('/login')

    # TODO: сообщение "что-то пошло не так :)"
    return redirect('/login')
