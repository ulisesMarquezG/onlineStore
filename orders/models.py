# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Product(models.Model):
    TYPE_CHOICES = (
        ('book',      u'Book'),
        ('electronic', u'Electronic'),
        ('clothing',  u'Clothing'),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='products/%Y/%m/%d/', blank=True, null=True)

    def __unicode__(self):
        # Retorna el nombre del producto como representación en texto
        return self.name

    def adjust_stock(self, delta):
        # Ajusta el stock: decrementa si delta es negativo, incrementa si es positivo
        # Valida que no se quede con stock negativo
        if self.stock + delta < 0:
            raise ValidationError(
                u"Stock insuficiente para {0}".format(self.name)
            )
        # Actualiza el stock de forma segura ante condiciones de carrera usando F()
        Product.objects.filter(pk=self.pk).update(stock=F('stock') + delta)
        # Refresca la instancia desde la base de datos
        self.refresh_from_db()

class Order(models.Model):
    STATUS_CHOICES = (
        ('cart',      u'En carrito'),
        ('confirmed', u'Confirmada'),
    )

    user = models.ForeignKey(User, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='cart'
    )

    def __unicode__(self):
        # Devuelve una cadena con el nombre del cliente y el estado legible
        display = dict(self.STATUS_CHOICES).get(self.status, self.status)
        return u"{0} — {1}".format(self.user.username, display)

    def get_total(self):
        # Calcula el total de la orden sumando el precio total de cada ítem
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        # Retorna la cantidad total de unidades de todos los ítems de la orden
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')

    def clean(self):
        # Valida antes de guardar: cantidad no mayor al stock disponible
        if self.pk is None and self.quantity > self.product.stock:
            raise ValidationError(u"No hay suficiente stock disponible")

    def save(self, *args, **kwargs):
        # Asigna unit_price desde el producto si no viene especificado
        if not self.unit_price and self.product:
            self.unit_price = self.product.unit_price

        # Determina si es un ítem nuevo o existente
        is_new = self.pk is None
        old_qty = 0
        if not is_new:
            # Obtiene la cantidad anterior para ajustar stock correctamente
            old_qty = OrderItem.objects.get(pk=self.pk).quantity

        # Guarda el ítem en la base de datos
        super(OrderItem, self).save(*args, **kwargs)

        # Calcula el cambio en stock y ajusta el producto
        delta = old_qty - self.quantity
        if delta != 0:
            self.product.adjust_stock(delta)

    def delete(self, *args, **kwargs):
        # Al eliminar el ítem, devuelve la cantidad al stock del producto
        self.product.adjust_stock(self.quantity)
        super(OrderItem, self).delete(*args, **kwargs)

    def __unicode__(self):
        # Representación en texto: nombre del producto y cantidad
        return u"{0} x {1}".format(self.product.name, self.quantity)

    def get_tax_rate(self):
        # Obtiene la tasa de impuesto según el tipo de producto
        rates = {'electronic': 0.16, 'clothing': 0.08, 'book': 0.0}
        return rates.get(self.product.type, 0.0)

    def get_tax_amount(self):
        """
        Calcula el importe de impuestos. Si faltan valores, retorna 0.0.
        """
        try:
            qty   = float(self.quantity)   if self.quantity   else 0.0
            price = float(self.unit_price) if self.unit_price else 0.0
        except (TypeError, ValueError):
            return 0.0
        return qty * price * self.get_tax_rate()
    get_tax_amount.short_description = 'Tax amount'

    def get_total_price(self):
        """
        Calcula el precio total (subtotal + impuestos). Protege contra None.
        """
        try:
            qty   = float(self.quantity)   if self.quantity   else 0.0
            price = float(self.unit_price) if self.unit_price else 0.0
        except (TypeError, ValueError):
            return 0.0
        subtotal = qty * price
        return subtotal + self.get_tax_amount()
    get_total_price.short_description = 'Total price'
