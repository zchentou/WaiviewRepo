from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.utils.safestring import mark_safe


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    occupation = forms.CharField(
        required=False, label='(If Applicable) Occupation/Current Level of Education and School')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'occupation',
                  'choice_view', 'timezone_to_use', 'picture']


class UserDeleteForm(forms.Form):
    delete_sure = forms.BooleanField(label='Delete My Account', required=False)


class EmailDeleteForm(forms.Form):
    delete_sure = forms.BooleanField(label='Remove My Emails', required=False)


class TermsSignUpForm(forms.Form):
    terms = forms.BooleanField(required=True, label=mark_safe(
        'I have read and agree to both the <a href="/terms/">Terms and Conditions</a> and <a href="/privacy/">Privacy Policy</a>'))

    def signup(self, request, user):
        user_profile = user.profile
        user_profile.terms = self.cleaned_data['terms']
        if not self.cleaned_data['terms']:
            raise forms.ValidationError(
                'You must accept both the terms and conditions and privacy policy to continue on Waiview while logged in')
        user.save()
        user_profile.save(update_fields=['terms'])
        return user
