from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render

from category.models import Category
from .models import Product

# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        "products": products,
        "product_count": product_count
    }
    return render(request, 'store/store.html', context)

def product_details(request, category_slug, product_slug):
    product_detail = Product.objects.get(category__slug=category_slug, slug=product_slug)

    context = {
        "product_detail": product_detail,
    }
    return render(request, "store/product-detail.html", context=context)