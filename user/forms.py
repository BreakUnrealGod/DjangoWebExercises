from django.forms import Form, ModelForm
from django import forms

from user.models import User


class RegisterForm(ModelForm):
    repassword = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = '__all__'
        exclude=['is_active',]


class LoginForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['is_active', 'email']