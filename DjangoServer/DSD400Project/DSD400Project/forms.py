from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label=""

        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label=""

        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label=""
        
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label="" 