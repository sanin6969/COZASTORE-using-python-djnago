from django import forms
from .models import Account
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
        
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number should contain numbers only.')
        if len(phone_number) != 10:
            raise forms.ValidationError('Phone number should be 10 digits.')
        
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        
        # Password validation 
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
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
            


  
 