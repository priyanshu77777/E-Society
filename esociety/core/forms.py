from django.contrib.auth.forms import UserCreationForm
from .models import Member,Complaint
from django import forms

class UserSignupForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['email','role','password1','password2']
        widgets = {
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["subject","description"]
        widgets = {
            "subject": forms.TextInput(attrs={"class":"input"}),
            "description": forms.Textarea(attrs={"class":"input"}),
        }
    