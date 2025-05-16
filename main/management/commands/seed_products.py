# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from orders.models import *


class Command(BaseCommand):
    help = "Crea productos de ejemplo para pruebas."

    def handle(self, *args, **options):
        productos = [
            {
                "name": "Libro de Django",
                "type": "book",
                "stock": 15,
                "unit_price": 299.90,
            },
            {
                "name": "Audífonos Bluetooth",
                "type": "electronic",
                "stock": 30,
                "unit_price": 899.00,
            },
            {
                "name": "Camiseta básica",
                "type": "clothing",
                "stock": 40,
                "unit_price": 129.50,
            },
        ]

        for data in productos:
            obj, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "type": data["type"],
                    "stock": data["stock"],
                    "unit_price": data["unit_price"],
                },
            )
