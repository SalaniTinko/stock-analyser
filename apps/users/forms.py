from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.core.validators import RegexValidator
alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class UploadAvatarForm(forms.Form):
    avatar = forms.FileField()

class StockTicker(forms.Form):
	ticker = forms.CharField(max_length=4,required=True,validators=[alphanumeric])