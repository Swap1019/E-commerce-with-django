from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserSellerInfo

class SignupForm(UserCreationForm):
    #User signup form
    email = forms.EmailField(max_length=200,required=True,widget= forms.EmailInput
                           (attrs={'placeholder':'Email','style':'margin-bottom:7px;'}))
    username = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Username','style':'margin-bottom:7px;'}))
    first_name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Firstname','style':'margin-bottom:7px;'}))
    last_name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Lastname','style':'margin-bottom:7px;'}))

    class Meta:
        model = User
        fields = ('profile','nickname','username','first_name','last_name','email')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password','style':'margin-bottom:7px;'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation','style':'margin-bottom:7px;'})
    
class UserProFileForm(forms.ModelForm):
    #User profileform
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')

        super(UserProFileForm, self).__init__(*args, **kwargs)  
        if not user.is_superuser:
            self.fields['first_name'].disabled = True
            self.fields['last_name'].disabled = True
            #self.fields['email'].help_text = "Change it if it was neccessary"
            self.fields['email'].disabled = True
            self.fields['is_seller'].disabled = True
    class Meta:
        #specifing the model and fields
        model = User
        fields = ['profile','nickname','username','email','first_name','last_name',
	        'is_seller']

class SellerRegisterForm(forms.ModelForm):
    #User SellerRegisterForm
    class Meta:
        model = UserSellerInfo
        fields = "__all__"
        exclude = ['user_id']


class SellerRequestApprove(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')
        
        super(SellerRequestApprove, self).__init__(*args, **kwargs) 
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True 
        self.fields['email'].disabled = True
        self.fields['is_seller'].help_text = "Accept this user as a Seller?"
        self.fields['is_staff'].disabled = True
        self.fields['date_joined'].disabled = True
        #admin_reject_reason is enabled
        #review_status is enabled
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_staff','is_seller','date_joined','admin_reject_reason']