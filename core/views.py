from django.shortcuts import render, redirect

# Mock Data
MOCK_HOUSES = [
    {
        'id': 1,
        'title': "Self-contain near Unilag Gate",
        'price': "350,000",
        'location': "Akoka, Yaba",
        'type': "Self-contain",
        'distance': "0.5km",
        'image': "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=500&q=80",
        'verified': True,
        'is_new': False,
        'description': "A lovely self-contain with running water and good security.",
        'agent_phone': "+2348000000000"
    },
    {
        'id': 2,
        'title': "2 Bedroom Flat Share",
        'price': "150,000",
        'location': "Bariga",
        'type': "Room",
        'distance': "2.5km",
        'image': "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=500&q=80",
        'verified': True,
        'is_new': True,
        'description': "Looking for a flatmate to share this spacious 2 bedroom flat.",
        'agent_phone': "+2348000000000"
    },
    {
        'id': 3,
        'title': "Studio Apartment",
        'price': "450,000",
        'location': "Onike",
        'type': "Self-contain",
        'distance': "1.2km",
        'image': "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=500&q=80",
        'verified': False,
        'is_new': True,
        'description': "Modern studio apartment recently renovated.",
        'agent_phone': "+2348000000000"
    }
]

MOCK_ROOMMATES = [
    {
        'id': 1,
        'name': "Chidinma O.",
        'budget': "100k - 150k",
        'location': "Yaba / Akoka",
        'tags': ["Quiet", "Non-smoker", "Christian"],
        'avatar': "https://ui-avatars.com/api/?name=Chidinma+O&background=random"
    },
    {
        'id': 2,
        'name': "Tunde B.",
        'budget': "200k",
        'location': "Surulere",
        'tags': ["Social", "Gamer", "Night-owl"],
        'avatar': "https://ui-avatars.com/api/?name=Tunde+B&background=random"
    },
    {
        'id': 3,
        'name': "Amina Y.",
        'budget': "120k",
        'location': "Anywhere near campus",
        'tags': ["Studious", "Clean"],
        'avatar': "https://ui-avatars.com/api/?name=Amina+Y&background=random"
    }
]

def home(request):
    context = {
        'featured_houses': MOCK_HOUSES[:2]
    }
    return render(request, 'home.html', context)

def houses(request):
    # Basic filtering logic could go here
    context = {
        'houses': MOCK_HOUSES
    }
    return render(request, 'houses.html', context)

def listing_detail(request, id):
    house = next((h for h in MOCK_HOUSES if h['id'] == int(id)), None)
    context = {
        'house': house
    }
    return render(request, 'listing_detail.html', context)

def roommates(request):
    context = {
        'roommates': MOCK_ROOMMATES
    }
    return render(request, 'roommates.html', context)

def post_listing(request):
    if request.method == 'POST':
        # Handle form submission logic here
        # For now, just redirect to houses
        return redirect('houses')
    return render(request, 'post.html')

def profile(request):
    return render(request, 'profile.html')

def my_listings(request):
    # Placeholder
    return redirect('profile')

def settings(request):
    # Placeholder
    return redirect('profile')

def logout_view(request):
    # Placeholder
    return redirect('home')
