from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200,widget= forms.EmailInput
                           (attrs={'placeholder':'Email','style':'margin-bottom:7px;'}))
    username = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Username','style':'margin-bottom:7px;'}))
    first_name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Firstname','style':'margin-bottom:7px;'}))
    last_name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Lastname','style':'margin-bottom:7px;'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password','style':'margin-bottom:7px;'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation','style':'margin-bottom:7px;'})