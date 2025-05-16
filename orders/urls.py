from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-to-cart/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/item/(?P<item_id>\d+)/delete/$', views.delete_cart_item, name='delete_cart_item'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^close-order/(?P<order_id>\d+)/$', views.close_order, name='close_order'),

]
