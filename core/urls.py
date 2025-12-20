from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('houses/', views.houses, name='houses'),
    path('houses/<int:id>/', views.listing_detail, name='listing_detail'),
    path('roommates/', views.roommates, name='roommates'),
    
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Protected
    path('post/', views.post_listing, name='post'),
    path('post-listing/', views.post_listing, name='post_listing'),
    path('profile/', views.profile, name='profile'),
    path('upload-verification/', views.upload_verification, name='upload_verification'),
    
    path('my-listings/', views.my_listings, name='my_listings'),
    path('settings/', views.settings, name='settings'),
]