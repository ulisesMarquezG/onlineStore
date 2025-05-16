# orders/admin.py

from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        'product',
        'quantity',
        'unit_price',
        'get_tax_amount',
        'get_total_price',
    )
    readonly_fields = (
        'unit_price',
        'get_tax_amount',
        'get_total_price',
    )

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'date',
        'get_total_items',
        'get_total',
    )
    list_filter = ('status',)
    readonly_fields = ('date',)
    inlines = [OrderItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'stock',
        'unit_price',
        'image'
    )
    list_editable = ('stock', 'unit_price')
    fields = (
        'name',
        'type',
        'stock',
        'unit_price',
        'image'
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
