from django.contrib import admin

from .models import Brand, Product, Stock, StockOut


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'product_type', 'gender', 'resale_price']
    search_fields = ['name', 'code']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'quantity', 'is_out_of_stock']
    list_filter = ['size']
    search_fields = ['product__name', 'product__code']


@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ['stock', 'user', 'quantity', 'date']
    list_filter = ['date', 'user']
    search_fields = ['stock__product__name', 'user__username']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]
