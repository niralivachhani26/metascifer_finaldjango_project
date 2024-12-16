from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, login_view, forgot_password, password_reset_confirm, get_cities, dashboard, profile, bidding, order, wishlists

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('get_cities/<str:state_name>/', get_cities, name='get_cities'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile ,name='profile'),
    path('bidding/', bidding, name='bidding'),
    path('order/', order, name='order'),
    path('wishlist/', wishlists, name='wishlist'),
]