from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    # profile_year        = blaaa blaa blaaa irrelevant.. You have your own stuff here don't worry about it

    # here is the important part.. add a class Meta-
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
