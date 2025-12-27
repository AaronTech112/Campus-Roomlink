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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '******'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '******'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'department', 'matric_number', 'password']
        labels = {
            'phone_number': 'WhatsApp Number',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '9012345678', 'maxlength': '10'}),
            'department': forms.TextInput(attrs={'placeholder': 'Computer Science'}),
            'matric_number': forms.TextInput(attrs={'placeholder': '2023/CP/CSC/0034'}),
        }
    
    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number')
        if matric_number:
            if len(matric_number) != 16:
                raise forms.ValidationError("Matric number must be exactly 16 characters.")
        return matric_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Ensure it's digits only
            if not phone_number.isdigit():
                 raise forms.ValidationError("WhatsApp number must contain digits only.")
            
            # Ensure exactly 10 digits
            if len(phone_number) != 10:
                raise forms.ValidationError("Please enter exactly 10 digits after +234.")
            
            # Prepend +234
            return "+234" + phone_number
        return phone_number

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
        fields = ['full_name', 'email', 'phone_number', 'department', 'matric_number', 'profile_picture']
        widgets = {
            'matric_number': forms.TextInput(attrs={'placeholder': '2023/CP/CSC/0034'}),
        }
    
    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number')
        if matric_number:
            if len(matric_number) != 16:
                raise forms.ValidationError("Matric number must be exactly 16 characters.")
        return matric_number
        
class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def to_python(self, data):
        if not data:
            return None
        if isinstance(data, list):
            return data
        return [data]

    def validate(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'], code='required')

class ListingForm(forms.ModelForm):
    title = forms.CharField(required=False) # Make title optional as it's not needed for Roommate requests
    images = MultipleFileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False, label="Upload Images (Select multiple)")
    videos = MultipleFileField(widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'video/*'}), required=False, label="Upload Videos (Optional, Max 2)")

    class Meta:
        model = Listing
        fields = ['title', 'description', 'rent', 'location', 'listing_type', 'image', 'gender_preference', 'level_preference', 'interests']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the house or roommate request...'}),
            'image': forms.HiddenInput(), # Hide the single image field, we will handle it in the view
        }
    
    def clean_videos(self):
        videos = self.cleaned_data.get('videos')
        if videos:
            if len(videos) > 2:
                raise forms.ValidationError("You can upload a maximum of 2 videos.")
            
            for video in videos:
                if video.size > 20 * 1024 * 1024:
                    raise forms.ValidationError(f"Video {video.name} exceeds the 20MB limit.")
        return videos
