from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import *


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        if commit:
            user.save()
        return user



class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User  # Assuming you have a User model
        fields = ('old_password', 'new_password1', 'new_password2')

class UpdateProfileForm(forms.ModelForm):
    facebook = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Facebook'}))
    twitter = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Twitter'}))
    linkedin = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin'}))

    class Meta:
        model = UserProfile
        fields = ('facebook', 'twitter', 'linkedin', 'bio')