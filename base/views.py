from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView
from .models import TheProduct,page_pic
from datetime import datetime,timedelta

class home(ListView):
    template_name = "base/home.html"
    #pass the products
    model = TheProduct
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        return context
    
class product(DetailView):
    template_name = 'base/view_product.html'
    context_object_name = 'product'
    model = TheProduct

    def get_object(self):
        id = self.kwargs.get('id')
        product = get_object_or_404(TheProduct,id=id)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        categories = product.category.all()  # Assuming a product can belong to multiple categories
        related_products = TheProduct.objects.filter(category__in=categories).exclude(id=product.id)
        context['related_products'] = related_products

        return context
    
class NewArrivalsView(ListView):
    template_name = "base/new-arrivals.html"
    context_object_name = "newproducts"
    queryset = TheProduct.objects.NewArrivals()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        return context