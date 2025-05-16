# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from orders.models import *

def home(request):
    usuario = request.user if request.user.is_authenticated else "invitado"
    products = Product.objects.filter(stock__gt=0)
    return render(request, "home.html", locals())


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Login automático tras registro (opcional)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, u"¡Registro exitoso! Ahora puedes comprar productos.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
