from django.contrib.auth.forms import UserCreationForm
from . models import UserCustom


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserCustom
        fields = UserCreationForm.Meta.fields
