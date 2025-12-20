from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('houses/', views.houses, name='houses'),
    path('houses/<int:id>/', views.listing_detail, name='listing_detail'),
    path('roommates/', views.roommates, name='roommates'),
    path('post/', views.post_listing, name='post'),
    path('post-listing/', views.post_listing, name='post_listing'), # For the form action
    path('profile/', views.profile, name='profile'),
    
    # Placeholders for links in profile/menus
    path('my-listings/', views.my_listings, name='my_listings'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]