from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, User
from .forms import SignupForm, LoginForm, ListingForm, VerificationForm
from django.db.models import Case, When, Value, IntegerField

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
        houses = houses.filter(location__icontains=q)
    
    budget = request.GET.get('budget')
    if budget:
        houses = houses.filter(rent__lte=budget)

    return render(request, 'houses.html', {'houses': houses})

def roommates(request):
    # Show roommate listings
    roommates = Listing.objects.filter(listing_type='roommate').order_by('-is_verified_listing', '-created_at')
    return render(request, 'roommates.html', {'roommates': roommates})

def listing_detail(request, id):
    house = get_object_or_404(Listing, id=id)
    return render(request, 'listing_detail.html', {'house': house})

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
            # Logic: Listings are NOT verified by default
            listing.is_verified_listing = False 
            listing.save()
            messages.success(request, "Listing posted successfully!")
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
    user_listings = Listing.objects.filter(posted_by=request.user)
    # Reusing houses template or create a specific one? 
    # For now redirect to profile where listings are shown
    return redirect('profile')

@login_required
def settings(request):
    # Placeholder
    return redirect('profile')
