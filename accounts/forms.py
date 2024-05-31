from django import forms
from .models import Account,UserProfile
import re

class RegistrationForm(forms.ModelForm):
    
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat Password',
        }))
    
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password','username']
        
        
    def clean(self): 
        cleaned_data=super(RegistrationForm,self).clean()
        
        
        # firstname and lastname validaton
        first_name=self.cleaned_data.get('first_name')
        last_name=self.cleaned_data.get('last_name')
        if not re.match("^[a-zA-Z]*$", first_name):
            raise forms.ValidationError(" first name Accepts only alphabetic characters.")
        if not re.match("^[a-zA-Z]*$", last_name):
            raise forms.ValidationError("last name Accepts only alphabetic characters.")
        
        # phone number validation
        phone_number = self.cleaned_data.get('phone_number')
        
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number should contain numbers only.')
        if len(phone_number) != 10:
            raise forms.ValidationError('Phone number should be 10 digits.')
        
        
        # Password validation 
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if len(password) > 8:
            raise forms.ValidationError('Password must be at  8 characters long.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'\d', password):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Password must contain at least one special character.')
        if password !=confirm_password:
            raise forms.ValidationError('Password does not match')
        
        
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            


class Userform(forms.ModelForm):
    class Meta:
        model =Account
        fields=('first_name','last_name','phone_number','email')
# class Userprofileform(forms.ModelForm):
#     profile_picture=forms.ImageField(required=False,error_messages={'invalid':{"imagefilesonly"}},widget=forms.FileInput)
#     class Meta:
#         model =UserProfile
#         fields=('address_line_1','address_line_2','profile_picture','city','state','country')
        
 