from django import forms
from .models import Account

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
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'