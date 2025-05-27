from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from users.models import CustomUser

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'phone_number', 'country']
