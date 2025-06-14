from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SpecialCompartmentType

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    allowed_compartments = forms.ModelMultipleChoiceField(
        queryset=SpecialCompartmentType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pokazuj również miejsca w:"
    )

    class Meta:
        model = UserProfile
        fields = ['default_start_station', 'default_end_station', 'allowed_compartments']
        labels = {
            'default_start_station': 'Domyślna stacja początkowa',
            'default_end_station': 'Domyślna stacja końcowa',
        }