from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView
from .models import the_product,page_pic,product_category
from django.http import JsonResponse
import json

class home(ListView):
    template_name = "base/home.html"
    #pass the products
    model = the_product
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        return context
    
class product(DetailView):
    template_name = 'base/view_product.html'
    context_object_name = 'product'
    model = the_product

    def get_object(self):
        id = self.kwargs.get('id')
        product = get_object_or_404(the_product.objects.all(),id=id)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        categories = product.category.all()  # Assuming a product can belong to multiple categories
        related_products = the_product.objects.filter(category__in=categories).exclude(id=product.id)
        context['related_products'] = related_products

        return context
