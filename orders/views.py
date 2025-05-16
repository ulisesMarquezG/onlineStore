# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Product, Order, OrderItem
from django.contrib import messages

@login_required(login_url='/accounts/login/')
@csrf_protect
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))

        if product.stock == 0:
            messages.error(request, u"No hay stock disponible para este producto.")
            return redirect('home')

        if quantity > product.stock:
            messages.warning(request, u"Solo hay %d unidades disponibles. Se agregó el máximo posible." % product.stock)
            quantity = product.stock

        # Buscar orden de carrito activa (no confirmada) para el usuario
        order = Order.objects.filter(user=request.user, status='cart').first()
        if not order:
            order = Order.objects.create(user=request.user, status='cart')

        # Verificar si el producto ya está en el carrito
        order_item = OrderItem.objects.filter(order=order, product=product).first()
        if order_item:
            # Si ya está, suma la cantidad
            nueva_cantidad = order_item.quantity + quantity
            if nueva_cantidad > product.stock:
                nueva_cantidad = product.stock
                messages.warning(request, u"Cantidad ajustada al stock disponible.")
            order_item.quantity = nueva_cantidad
            order_item.save()
        else:
            # Si no, crea el nuevo item
            OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=product.unit_price)

        messages.success(request, u"Producto agregado al carrito.")
        return redirect('home') 
    return redirect('home')

@login_required
def delete_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id, order__user=request.user, order__status='cart')
    order_item.delete()
    return redirect('orders:cart')

@login_required(login_url='/accounts/login/')
def cart(request):
    order = Order.objects.filter(user=request.user, status='cart').first()
    order_items = order.items.all() if order else []
    return render(request, "cart.html", {
        'order': order,
        'order_items': order_items
    })

@login_required
@csrf_protect
def close_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='cart')
    if request.method == 'POST':
        order.status = 'confirmed'
        order.save()
        messages.success(request, u"¡Orden confirmada! Gracias por tu compra.")
        return redirect('home')
    return redirect('cart')