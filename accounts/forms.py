# from django.forms import ModelForm
from django import forms
from . models import Account,UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm,PasswordChangeForm


class Registrationform(forms.ModelForm):
    password=forms.CharField(validators=[validate_password],widget=forms.PasswordInput(attrs={'placeholder':'enter password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
    def __init__(self,*args, **kwargs):
        super(Registrationform,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'
        self.fields['email'].widget.attrs['placeholder']='Enter email'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    
   
    def clean(self):
        cleaned_data=super(Registrationform,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
    def clean_phone(self):
        phone= self.cleaned_data["phone"]
        if Account.objects.filter(phone=phone).exists():
            raise ValidationError("An user with this phone number already exists!")
        return phone
    

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number']
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control' 

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        fields=['address_line_1','address_line_2','city','state','country','profile_picture']
        model=UserProfile
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
