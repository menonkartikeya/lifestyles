from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = ('username', 'mobno', 'gender','height','weight','target','diets','bill','foodplans','lives','age','allotnutri','allotdieti','allottrain','sub','bio','location','address')

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = ('username', 'mobno', 'gender','height','weight','target','diets','bill','foodplans','lives','age','allotnutri','allotdieti','allottrain','sub','bio','location','address')