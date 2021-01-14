from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Portfolio
from django.forms import ModelForm, TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import FileInput, ClearableFileInput

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'login-signup-form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login-signup-form-control', 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'login-signup-form-control','placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login-signup-form-control','placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login-signup-form-control','placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['username'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'Confirm Password'})

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['username'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Username'})
        self.fields['email'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Last Name'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'company', 'cover_image']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = ''
        self.fields['image'].widget = CustomClearableFileInput(attrs={'class': 'profile-image-upload'})

        self.fields['cover_image'].label = ''
        self.fields['cover_image'].widget = CustomClearableFileInput(attrs={'class': 'profile-cover-image-upload'})

        self.fields['company'].label = ''
        self.fields['company'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Company Name'})

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'Confirm New Password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(PasswordChangingForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

class PasswordResettingForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'login-signup-form-control','placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(PasswordResettingForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ''

class PasswordResetConfirmingForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login-signup-form-control','placeholder': 'Confirm New Password'}))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(PasswordResetConfirmingForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''

class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['portfolio_name']

    def __init__(self, *args, **kwargs):
        super(PortfolioCreateForm, self).__init__(*args, **kwargs)
        self.fields['portfolio_name'].label = ''
        self.fields['portfolio_name'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'NAME'})

class PortfolioUpdateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['portfolio_name']

    def __init__(self, *args, **kwargs):
        super(PortfolioUpdateForm, self).__init__(*args, **kwargs)
        self.fields['portfolio_name'].label = ''
        self.fields['portfolio_name'].widget = TextInput(attrs={'class': 'login-signup-form-control', 'placeholder': 'Update Portfolio'})


#-------------------------------------------------------------------------------
#------------------------------OVERRIDE WIDGETS---------------------------------
#-------------------------------------------------------------------------------
class CustomClearableFileInput(ClearableFileInput):
    template_name = "users/override_clearable_file_input.html"
