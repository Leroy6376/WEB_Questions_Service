from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={ 'label' : 'login', 'class': 'form-control form-control-lg', 'placeholder': 'Your user name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your password'}))