from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from carts.models import Cart, CartItem
from category.models import Category
from .models import Product
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        product_count = products.count()
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    context = {
        "products": paged_products,
        "product_count": product_count,
    }
    return render(request, 'store/store.html', context)

def product_details(request, category_slug, product_slug):
    product_detail = Product.objects.get(category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product_detail).exists()
    context = {
        "product_detail": product_detail,
        "in_cart": in_cart,
    }
    return render(request, "store/product-detail.html", context=context)