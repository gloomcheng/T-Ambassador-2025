from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'phone']
        widgets = {
            'gender': forms.RadioSelect(choices=UserProfile.GENDER_CHOICES)
        }