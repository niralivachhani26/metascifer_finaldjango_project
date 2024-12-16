from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('about', views.about, name='about'),
    path('how_to_bid', views.how_to_bid, name='how_to_bid'),
    path('how_to_sell', views.how_to_sell, name='how_to_sell'),
    path('terms_condition', views.terms_condition, name='terms_condition'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('art_catalog/<int:user_id>', views.art_list, name='art_catalog'),
    path('art_catalogs/<int:category_id>', views.art_list1, name='art_catalogs'),
    path('add_wishlist/<int:art_id>', views.add_wishlist, name="add_wishlist"),
    path('art_detail/<int:art_id>', views.art_details, name="art_detail"),
    path('place_bid', views.place_bid, name="place_bid"),
    path('artist_detail/<int:user_id>', views.artist_detail, name="artist_detail"),
]