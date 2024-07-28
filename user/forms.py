from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
    )
from .models import (
    User,
    UserSellerInfo,
    ReportedProduct,
    )
from base.models import TheProduct,Images
from .mixins import SpecsJsonFieldValidationMixin

class SignUpForm(UserCreationForm):
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
        fields = ['profile','nickname','username','first_name','last_name','email']
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password','style':'margin-bottom:7px;'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation','style':'margin-bottom:7px;'})
    
class UserProfileForm(UserChangeForm):
    #User profileform
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')
        super(UserProfileForm, self).__init__(*args, **kwargs)

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
        
        widgets = {
            'profile': forms.FileInput(attrs={'accept': 'image/*'}),  # Add accept attribute for image files
        }

class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=150, required=True, label='Username')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if email and username:
            try:
                user = User.objects.get(email=email, username=username)
            except User.DoesNotExist:
                raise forms.ValidationError("There is no user registered with the specified email address and username.")
        return cleaned_data


class SellerRegisterForm(forms.ModelForm):
    #User SellerRegisterForm

    class Meta:
        model = UserSellerInfo
        fields = '__all__'
        exclude = ['user_id']


class SellerRequestApproveForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')
        
        super(SellerRequestApproveForm, self).__init__(*args, **kwargs) 
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
        fields = ['username','first_name','last_name','email','is_staff','is_seller','date_joined']

class NewProductApproveForm(SpecsJsonFieldValidationMixin,forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(NewProductApproveForm, self).__init__(*args, **kwargs) 
        self.fields['created_by'].disabled = True

    class Meta:
        model = TheProduct
        fields = ['pic_sample','product','created_by','category','price','discount_percentage','description','specs','availability']

class AddProductForm(SpecsJsonFieldValidationMixin,forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs) 
        self.fields['availability'].disabled = True

    class Meta:
        model = TheProduct
        fields = ['product','category','price','discount_percentage','pic_sample','description','specs','availability']


class ReportProductForm(forms.ModelForm):
    class Meta:
        model = ReportedProduct
        fields = '__all__'
        exclude = ['id','reported_product','user','checked']

class ProductUpdateForm(SpecsJsonFieldValidationMixin,forms.ModelForm):
    class Meta:
        model = TheProduct
        fields = ['product','category','price','discount_percentage','pic_sample','description','specs','quantity','availability']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['availability'].choices = (
            ('A','Available'),
            ('U','Unavailable'),
            )
        self.fields['product'].disabled = True
        if self.instance.availability in ['B', 'I']:
            self.fields['availability'].disabled = True

    def clean_availability(self):
        availability = self.cleaned_data.get('availability')
        return availability
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = '__all__'
        exclude = ['product']