from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
import json

def load_states():
    with open('account/indian_states_cities.json', 'r') as f:
        data = json.load(f)
    return [(state, state) for state in data["states"].keys()]

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    state = forms.ChoiceField(choices=load_states(),required=True)
    city = forms.CharField(required=True)  # This will be dynamically filled via AJAX
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput,required=True)
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control','style':'display:none;'}),
        required=False,
        label=""
        # Initially not required
    )

    dob = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date of Birth",
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['usertype','name', 'email','password','confirm_password', 'dob', 'contact_no','profile','address','state','city','zipcode']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        usertype = cleaned_data.get('usertype')
        description = cleaned_data.get('description')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        if usertype == 'artist' and not description:
            self.add_error('description', "Description is required for artists.")

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

    usertype = forms.ChoiceField(
        choices=[('artist', 'Artist'), ('customer', 'Customer')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'usertype']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Enter your registered email')

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    state = forms.ChoiceField(choices=load_states())
    city = forms.CharField()  # This will be dynamically filled via AJAX

    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Address",
        required=True
    )

    dob = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date of Birth"
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'dob', 'contact_no', 'profile', 'address', 'state',
                  'city', 'zipcode']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class PasswordUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['password','confirm_password']

    def __init__(self, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

