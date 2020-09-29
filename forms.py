from django import forms
from django.contrib.auth.models import User
class Login(forms.Form):
    phonenum1=forms.IntegerField()
    password9=forms.CharField(max_length=30,widget=forms.PasswordInput(
    attrs={
        'placeholder':'PASSWORD'}))
    
    def clean_phonenum1(self,*args,**kwargs):
        phonenum1=self.cleaned_data["phonenum1"]
        print(phonenum1)
        if len(str(phonenum1))<10:
            raise forms.ValidationError("PLEASE ENTER VALID NUMBER")
        return phonenum1
    
    def clean_password9(self,*args,**kwargs):
        b=self.cleaned_data.get("password9")
        if len(b)<8:
            raise forms.ValidationError("ENTER VALID PASSWORD")
        return b
            
