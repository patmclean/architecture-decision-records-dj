"""Custom User Forms."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form."""

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    """Custom USer Change Form."""

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )
