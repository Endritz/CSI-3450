from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MonetaryInfo
from django.core.validators import MinValueValidator



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DepositForm(forms.Form):
    depositUSD = forms.DecimalField(required = False, max_digits = 6, decimal_places= 2, widget=forms.TextInput(attrs={'placeholder': '0'}), validators = [MinValueValidator(0, message = 'please do not put in negative numbers')])
    depositCAD = forms.DecimalField(required = False, max_digits = 6, decimal_places= 2, widget=forms.TextInput(attrs={'placeholder': '0'}), validators = [MinValueValidator(0, message = 'please do not put in negative numbers')])

class WithdrawForm(forms.Form):
    withdrawUSD = forms.DecimalField(required = False,max_digits = 6, decimal_places= 2,  widget=forms.TextInput(attrs={'placeholder': '0'}), validators = [MinValueValidator(0, message = 'please do not put in negative numbers')])
    withdrawCAD = forms.DecimalField(required = False, max_digits = 6, decimal_places= 2, widget=forms.TextInput(attrs={'placeholder': '0'}), validators = [MinValueValidator(0, message = 'please do not put in negative numbers')])

    