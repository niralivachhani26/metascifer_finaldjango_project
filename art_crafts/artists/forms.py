from django import forms
from django.apps import apps
from .models import Arts, Category
from django.contrib.auth import get_user_model
import json

CustomUser = apps.get_model('account', 'CustomUser')

def load_states():
    with open('account/indian_states_cities.json', 'r') as f:
        data = json.load(f)
    return [(state, state) for state in data["states"].keys()]

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
                  'city', 'zipcode','description']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ArtsForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Fetch all categories
        widget=forms.Select(attrs={'class': 'form-control'})  # Add CSS classes
    )

    title = forms.CharField(required=True)
    auction_date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Auction Date"
    )
    auction_min_price = forms.DecimalField()


    class Meta:
        model = Arts
        fields = ['title', 'art_image','auction_date_time', 'auction_min_price', 'size', 'framing', 'theme', 'signature',
                  'authenticity', 'narrative', 'guidelines', 'artist_style','notable_work','category']

    def __init__(self, *args, **kwargs):
        super(ArtsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'