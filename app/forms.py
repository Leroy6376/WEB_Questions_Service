from dataclasses import fields
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(label="User name", widget=forms.TextInput(attrs={'class': 'form-control-lg', 'placeholder': 'Your user name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control-lg', 'placeholder': 'Your password'}))

    def clean(self):
        data = super().clean()
        if not self.errors and not auth.authenticate(username=data.get("username"), password=data.get("password")):
            raise forms.ValidationError("Sorry, wrong password or login! Try again.")
    

class RegistrationForm(forms.Form):
    username = forms.CharField(label="User name", widget=forms.TextInput(attrs={'class': 'form-control-lg', 'placeholder': 'Your user name'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control-lg', 'placeholder': 'Your email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control-lg', 'placeholder': 'Your password'}))
    repeat_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-control-lg', 'placeholder': 'Repeat your password'}))
    avatar =  forms.ImageField(label="Your avatar", required=False)

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

        if password != repeat_password:
            raise forms.ValidationError("Passwords mismatch")
        return repeat_password

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("A user with the same name already exists")
        return data


class QuestionForm(forms.ModelForm):
    header = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control-lg'}))
    body = forms.CharField(label="Text", widget=forms.Textarea(attrs={'class': 'form-control-lg'}))
    tags = forms.ModelMultipleChoiceField(queryset=models.Tag.objects.get_queryset(), widget=forms.SelectMultiple(attrs={'style': 'height:200px'}))
    new_tag = forms.CharField(label="New tags", required=False, widget=forms.TextInput(attrs={'class': 'form-control-lg'}))

    class Meta:
        model = models.Question
        fields = ['header', 'body', 'tags']

    def clean_new_tag(self):
        data = self.cleaned_data['new_tag']
        tags = data.split()
        for d in tags:
           if models.Tag.objects.filter(name=d).exists():
               raise forms.ValidationError(('This tag already exists: %(value)s'), params={'value': d})
        return data

class AnswerForm(forms.ModelForm):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control-lg', 'style': 'height:150px', 'name' : ''}))
    
    class Meta:
        model = models.Answer
        fields = ['body']

    def __init__(self, *args, **kwargs):
        disabled = kwargs.pop('disabled', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if disabled:
            self.fields['body'].disabled = True

class ProfileForm(forms.ModelForm):
    username = forms.CharField(label="User name", widget=forms.TextInput(attrs={'class': 'form-control-lg'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control-lg'}))
    avatar = forms.ImageField(label="Avatar", required=False)
    class Meta:
        model = User
        fields = ['username', 'email']
