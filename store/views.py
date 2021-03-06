from django.core.checks import messages
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from category.models import Category
from store.forms import ReviewForm
from .models import Product, ReviewRating
from carts.views import _cart_id
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.contrib import messages


# Create your views here.
def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        product_count = products.count()
        paginator = Paginator(products, 3)
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


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET.get("keyword")
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    if request.method == "POST":
        url = request.META.get("HTTP_REFERER")
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)