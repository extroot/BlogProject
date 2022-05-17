from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from user.models import CustomUser


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password1',
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
