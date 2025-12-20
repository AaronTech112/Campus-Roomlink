from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None # We use email as username
    email = models.EmailField(_('email address'), unique=True)
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100, blank=True, null=True)
    matric_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Verification
    is_verified_student = models.BooleanField(default=False)
    
    VERIFICATION_STATUS_CHOICES = [
        ('not_submitted', 'Not Submitted'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='not_submitted'
    )
    
    # Secure upload for ID/Admission Letter
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def trust_label(self):
        if self.is_verified_student:
            return "Verified Student"
        return "Unverified Student"

    @property
    def whatsapp_link(self):
        # Remove any non-digit characters
        clean_number = ''.join(filter(str.isdigit, str(self.phone_number)))
        # If it starts with '0', replace with '234' (assuming Nigerian context as per requirements)
        if clean_number.startswith('0'):
            clean_number = '234' + clean_number[1:]
        return clean_number


class Listing(models.Model):
    LISTING_TYPE_CHOICES = [
        ('house', 'House'),
        ('roommate', 'Roommate'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    
    # Simple single image for MVP
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_verified_listing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def verification_badge(self):
        if self.is_verified_listing:
            return "Verified Listing"
        if self.posted_by.is_verified_student:
            return "Listing Under Review"
        return "Unverified User – Under Review"
