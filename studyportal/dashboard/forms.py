from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from .models import *
class NotesForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model=Notes
        fields=['title','description']
    
class DateInput(forms.DateInput):
    input_type='date'
    
class HomeworkForm(forms.ModelForm):

    class Meta:
        model=Homework
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due': forms.DateInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            # 'status': forms.Boo(attrs={'class': 'form-control'}),
        }
        fields=['subject','title','description','due','status']

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','status']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'})
        }
class ConversionForm(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect())

class ConversionLengthForm(forms.Form):
    CHOICES=[('metre','Metre'),('centi','Centi')]
    input_length=forms.FloatField(initial=0,label=False,widget=forms.NumberInput(attrs={"class":"form-control"}))
    input_unit=forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-control"}),label=False)
    output_unit=forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-control"}),label=False)

class ConversionMassForm(forms.Form):
    CHOICES=[('gram','Gram'),('centi','Centi')]
    input_mass=forms.FloatField(initial=0,label=False,widget=forms.NumberInput(attrs={"class":"form-control"}))
    input_unit=forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-control"}),label=False)
    output_unit=forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-control"}),label=False)

from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# note USer model contains only three columns--username, email, password

# model--->class---->models.Model
# form---->class---->forms.Form
# forms.py

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
