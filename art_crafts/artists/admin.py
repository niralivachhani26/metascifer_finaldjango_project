from django.contrib import admin
from .models import Category, Arts, wishlist, Bid

admin.site.register(Category)
admin.site.register(Arts)
admin.site.register(wishlist)
admin.site.register(Bid)
# Register your models here.
