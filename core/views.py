from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, User, ListingImage
from .forms import SignupForm, LoginForm, ListingForm, VerificationForm, ProfileUpdateForm
from django.db.models import Case, When, Value, IntegerField, Q

# --- Public Views ---

def home(request):
    # Featured listings: Verified listings first, then recent
    featured_houses = Listing.objects.all().order_by(
        '-is_verified_listing', '-created_at'
    )[:5]
    return render(request, 'home.html', {'featured_houses': featured_houses})

def houses(request):
    # Sort: Verified listings higher
    # Logic: 
    # 1. Verified Listing (Highest)
    # 2. Verified User
    # 3. Unverified
    
    # Simple sorting by verified listing boolean first
    houses = Listing.objects.filter(listing_type='house').order_by('-is_verified_listing', '-created_at')
    
    # Filter logic (basic)
    q = request.GET.get('q')
    if q:
        houses = houses.filter(
            Q(location__icontains=q) | 
            Q(title__icontains=q) | 
            Q(description__icontains=q)
        )
    
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    
    if min_budget:
        houses = houses.filter(rent__gte=min_budget)
    if max_budget:
        houses = houses.filter(rent__lte=max_budget)

    return render(request, 'houses.html', {'houses': houses})

def roommates(request):
    # Show roommate listings
    roommates = Listing.objects.filter(listing_type='roommate').order_by('-is_verified_listing', '-created_at')
    
    # Filter logic
    q = request.GET.get('q')
    if q:
        roommates = roommates.filter(
            Q(location__icontains=q) | 
            Q(title__icontains=q) | 
            Q(description__icontains=q) |
            Q(interests__icontains=q) |
            Q(posted_by__full_name__icontains=q)
        )
    
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')
    
    if min_budget:
        roommates = roommates.filter(rent__gte=min_budget)
    if max_budget:
        roommates = roommates.filter(rent__lte=max_budget)
        
    gender = request.GET.get('gender')
    if gender:
        roommates = roommates.filter(gender_preference=gender)

    return render(request, 'roommates.html', {'roommates': roommates})

def listing_detail(request, id):
    house = get_object_or_404(Listing, id=id)
    
    # Increment view count
    house.views_count += 1
    house.save()
    
    interests_list = []
    if house.interests:
        interests_list = [i.strip() for i in house.interests.split(',')]
    return render(request, 'listing_detail.html', {'house': house, 'interests_list': interests_list})

def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_listings = Listing.objects.filter(posted_by=profile_user).order_by('-created_at')
    return render(request, 'user_profile.html', {'profile_user': profile_user, 'user_listings': user_listings})

# --- Auth Views ---

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Welcome to RoomLink.")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- Protected Views ---

@login_required
def profile(request):
    user_listings = Listing.objects.filter(posted_by=request.user)
    return render(request, 'profile.html', {'user_listings': user_listings})

@login_required
def post_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.posted_by = request.user
            listing.is_verified_listing = False 
            
            # Handle images
            images = request.FILES.getlist('images')
            if images:
                # Set the first image as the main thumbnail
                listing.image = images[0]
            
            # Auto-generate title for Roommate listings if missing
            if listing.listing_type == 'roommate':
                if not listing.title:
                    listing.title = f"Roommate Request - {request.user.full_name}"
                
                # Handle multi-select interests
                interests_list = request.POST.getlist('interests_list')
                if interests_list:
                    listing.interests = ",".join(interests_list)
            
            listing.save()
            
            # Save all images to gallery
            if images:
                for img in images:
                    ListingImage.objects.create(listing=listing, image=img)

            messages.success(request, "Listing posted successfully!")
            
            # Redirect based on type
            if listing.listing_type == 'roommate':
                return redirect('roommates')
            return redirect('houses')
    else:
        form = ListingForm()
    return render(request, 'post.html', {'form': form})

@login_required
def upload_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_status = 'pending' # Set to pending review
            user.save()
            messages.success(request, "Document uploaded. Admin will review shortly.")
            return redirect('profile')
    else:
        form = VerificationForm(instance=request.user)
    return render(request, 'auth/upload_verification.html', {'form': form})

@login_required
def my_listings(request):
    user_listings = Listing.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'my_listings.html', {'user_listings': user_listings})

@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id, posted_by=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listing = form.save(commit=False)
            
            # Handle new images
            images = request.FILES.getlist('images')
            if images:
                # If no main image exists, use the first new one
                if not listing.image:
                    listing.image = images[0]
                
                # Add to gallery
                for img in images:
                    ListingImage.objects.create(listing=listing, image=img)
            
            # Handle multi-select interests for roommates
            if listing.listing_type == 'roommate':
                interests_list = request.POST.getlist('interests_list')
                if interests_list:
                    listing.interests = ",".join(interests_list)
                    
            listing.save()
            messages.success(request, "Listing updated successfully!")
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'post.html', {'form': form, 'is_edit': True})

@login_required
def delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id, posted_by=request.user)
    listing.delete()
    messages.success(request, "Listing deleted successfully.")
    return redirect('my_listings')

@login_required
def settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('settings')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'settings.html', {'form': form})
