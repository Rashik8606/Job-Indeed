from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import JobVacancies



class CustomCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=200, required=False)
    about_me = forms.CharField(widget=forms.Textarea, required=False)
    skill = forms.CharField(max_length=200, required=False)
    experience = forms.CharField(widget=forms.Textarea, required=False)
    education = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(required=False)
    location = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','profile_picture']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



class JobVacanciesForm(forms.ModelForm):
    class Meta:
        model = JobVacancies
        fields = ['jobTitle', 'branchEmail', 'jobQualification', 'location', 'contactNumber', 'applicationEmailUrl', 'jobSkill', 'jobType', 'jobSalary', 'shortDiscription', 'jobResposibility','workingEnvironment','jobRequirement', 'jobCategory','companyLogo']


class JobSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)