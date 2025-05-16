# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Product, Order, OrderItem
from django.http import HttpResponse

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

def export_confirmed_orders_txt(modeladmin, request, queryset):
    """
    Exporta órdenes confirmadas a un archivo TXT.
    """
    # Solo selecciona órdenes confirmadas
    orders = queryset.filter(status='confirmed').order_by('date')

    lines = []
    for order in orders:
        lines.append(u"Orden #{0} - Usuario: {1} - Fecha: {2}".format(
            order.id, order.user.username, order.date.strftime('%Y-%m-%d %H:%M')
        ))
        for item in order.items.all():
            lines.append(u"   - {0} x{1} @ {2} MXN (Impuestos: {3} MXN)".format(
                item.product.name,
                item.quantity,
                item.unit_price,
                item.get_tax_amount()
            ))
        lines.append(u" Total: {0} MXN".format(order.get_total()))
        lines.append(u"-" * 50)

    response = HttpResponse(
        u'\n'.join(lines).encode('utf-8'),
        content_type='text/plain; charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename=ordenes_confirmadas.txt'
    return response

export_confirmed_orders_txt.short_description = u"Exportar órdenes confirmadas a TXT"
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
    actions = [export_confirmed_orders_txt]
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
