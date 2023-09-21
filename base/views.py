from django.shortcuts import render
from django.views.generic import ListView,TemplateView
from .models import the_product

class home(ListView):
    template_name = "base/home.html"
    context_object_name = 'products'
    model = the_product
