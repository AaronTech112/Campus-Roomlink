from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, ListingImage
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'full_name', 'phone_number', 'is_verified_student', 'verification_status')
    list_filter = ('is_verified_student', 'verification_status')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'department', 'matric_number')}),
        ('Verification', {'fields': ('is_verified_student', 'verification_status', 'verification_document')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2', 'full_name', 'phone_number', 'department'),
        }),
    )
    
    ordering = ('email',)
    
    actions = ['approve_verification', 'reject_verification']

    def approve_verification(self, request, queryset):
        rows_updated = queryset.update(verification_status='approved', is_verified_student=True)
        self.message_user(request, f"{rows_updated} users verified.")
    approve_verification.short_description = "Approve selected users' verification"

    def reject_verification(self, request, queryset):
        rows_updated = queryset.update(verification_status='rejected', is_verified_student=False)
        self.message_user(request, f"{rows_updated} users verification rejected.")
    reject_verification.short_description = "Reject selected users' verification"


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing_type', 'posted_by', 'is_verified_listing', 'created_at')
    list_filter = ('listing_type', 'is_verified_listing')
    search_fields = ('title', 'location', 'posted_by__email')
    inlines = [ListingImageInline]
    
    actions = ['verify_listings']

    def verify_listings(self, request, queryset):
        queryset.update(is_verified_listing=True)
    verify_listings.short_description = "Mark selected listings as Verified"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Listing, ListingAdmin)
