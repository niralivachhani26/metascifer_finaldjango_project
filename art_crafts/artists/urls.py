from django.urls import path
from .views import dashboard, profile, bidding, order,arts, add_arts, edit_arts, delete_arts

urlpatterns = [
    path('dashboard_artist/', dashboard, name='dashboard_artist'),
    path('profile_artist/', profile ,name='profile_artist'),
    path('bidding_artist/', bidding, name='bidding_artist'),
    path('order_artist/', order, name='order_artist'),
    path('arts/', arts, name='arts'),
    path('add_arts/', add_arts, name='add_arts'),
    path('edit_arts/<int:pk>/', edit_arts, name='edit_arts'),
    path('delete_arts/<int:pk>', delete_arts, name='delete_arts'),
]