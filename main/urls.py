# main/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
]