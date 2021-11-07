from .models import Category
from carts.models import Cart

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
