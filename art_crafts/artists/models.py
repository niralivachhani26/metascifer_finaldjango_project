from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Arts(models.Model):
    title = models.CharField(max_length=255)
    art_image = models.ImageField(blank=True,upload_to='static/images/arts/')
    auction_date_time =models.DateTimeField()
    auction_min_price = models.DecimalField(max_digits=5,decimal_places=2)
    size = models.CharField(max_length=255)
    framing = models.BooleanField(default=False)
    theme = models.CharField(max_length=255)
    signature = models.CharField(max_length=200)
    authenticity = models.CharField(max_length=200)
    narrative = models.TextField()
    guidelines = models.TextField()
    artist_style = models.TextField()
    notable_work = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the current user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.name}"

class wishlist(models.Model):
    art = models.ForeignKey(Arts, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Bid(models.Model):
    art = models.ForeignKey(Arts, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bid_price = models.DecimalField(blank=True, null=True,max_digits=5,decimal_places=2)
    STATUS_CHOICES = [
        ('cancel', 'Cancel'),
        ('process', 'Process'),
        ('win', 'Win'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='process')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.art.title}"
# Create your models here.
