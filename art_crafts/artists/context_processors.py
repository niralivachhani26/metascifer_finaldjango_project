from .models import Category

def category_menu(request):
    categories = Category.objects.all()  # Fetch all categories
    return {'categories': categories}