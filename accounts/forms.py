from datetime import date
from django.forms.extras.widgets import SelectDateWidget
from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form to edit user profile information"""
    date_of_birth = forms.DateField(widget=SelectDateWidget(empty_label=("Year", "Month", "Day"),
                                                            years=(range(date.today().year-95, date.today().year-5))))

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',
                  'date_of_birth', 'bio', 'avatar')

    def clean(self):
        cleaned_data = super().clean()

        bio = cleaned_data.get('bio')
        if len(bio) < 10 and len(bio) != 0:
            raise forms.ValidationError('Bio must be at least 10 characters')

        return cleaned_data


class EmailForm(forms.ModelForm):
    """Form to edit user email"""
    verify_email = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('email', 'verify_email')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify_email = cleaned_data.get('verify_email')
        if email != verify_email:
            raise forms.ValidationError('Emails do not match')

        return cleaned_data
