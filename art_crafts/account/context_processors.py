from .models import CustomUser

def artist_menu(request):
    artist = CustomUser.objects.filter(usertype='artist')  # Fetch all categories
    return {'artists': artist}