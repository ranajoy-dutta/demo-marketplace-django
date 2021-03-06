from django.contrib import admin
from .models import Product, Variation
from .models import ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'modified_date',
        'is_available'
    )

    prepopulated_fields = {
        'slug': ('product_name',)
    }


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
        'created_date',
    )

    list_editable = (
        'is_active',
    )


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
