from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Listing

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'department')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'department', 'is_verified_student', 'verification_status')

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'department', 'matric_number', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class VerificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['verification_document']
        widgets = {
            'verification_document': forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'})
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']
        
class ListingForm(forms.ModelForm):
    title = forms.CharField(required=False) # Make title optional as it's not needed for Roommate requests

    class Meta:
        model = Listing
        fields = ['title', 'description', 'rent', 'location', 'listing_type', 'image', 'gender_preference', 'level_preference', 'interests']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the house or roommate request...'}),
        }
