from django.contrib.auth.forms import AuthenticationForm

from user.models import CustomUser


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password1',
        ]
