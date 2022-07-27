from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post


class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class' : "form-control",
            'id' : "inputUsername"
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'id' : "inputPassword"
        })
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'id' : "ReInputPassword"
        })
    )

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class' : "form-control",
            'id' : "InputEmail"
        })
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class' : "form-control",
            'id' : "InputFirst_name"
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class' : "form-control",
            'id' : "InputLast_name"
        })
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают'
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):

    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class' : "form-control",
            'id' : "inputUsername"
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'id' : "inputPassword"
        })
    )


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['h1', 'text', 'image',]
        widgets = {
            'h1' : forms.TextInput(attrs={'class' : "form-input"}),
            'text' : forms.Textarea(attrs={'column' : 60, 'rows' : 10}),
        } 