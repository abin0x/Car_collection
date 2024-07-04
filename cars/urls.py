

from django.urls import path
from .views import HomeView, CarDetailView, RegisterView, ProfileView, BuyCarView, user_logout
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('brand/<slug:brand_slug>/', HomeView.as_view(), name='brand_wise'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('buy/<int:pk>/', BuyCarView.as_view(), name='buy_car'),
    path('logout/', user_logout, name='logout'),
    path('login/',views.UserLoginView.as_view(),name='user_login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/edit',views.edit_profile,name='edit_profile'),
    
    # Other URL patterns...
]
