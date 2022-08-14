from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from movies import models

User = get_user_model()


class MovieForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(
        User.objects.all(),
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = models.Movie
        fields = ["name", "plot", "created_by"]


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is taken")
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = User
        fields = ["username", "password"]
