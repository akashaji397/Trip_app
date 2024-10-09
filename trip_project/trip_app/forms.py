# forms.py
from django import forms
from .models import Trip  # It's better to import the specific model

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip  # Corrected from 'models' to 'model'
        fields = '__all__'  # This is correct if you want to include all fields
    