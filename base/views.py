from django.db.models import Q,Count
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import ListView,DetailView
from .models import TheProduct,page_pic
from user.models import User
from datetime import datetime,timedelta

class home(ListView):
    template_name = "base/list_page.html"
    #pass the products
    context_object_name = 'products'
    model = TheProduct
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
        return context
    
class product(DetailView):
    template_name = 'base/view_product.html'
    context_object_name = 'product'
    model = TheProduct
    #gets the specified product
    def get_object(self):
        id = self.kwargs.get('id')
        product = get_object_or_404(TheProduct,id=id)
        print(product.comments)

        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)

        return product
    
    #returns the related product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        categories = product.category.all()  # Assuming a product can belong to multiple categories
        related_products = TheProduct.objects.filter(category__in=categories).exclude(id=product.id)
        context['related_products'] = related_products
        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile

        return context
    
class NewArrivalsView(ListView):
    template_name = "base/list_page.html"
    context_object_name = "products"
    queryset = TheProduct.objects.newarrivals()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        context['user_profile'] = User.objects.get().profile
        return context
    
class MostViewedProducts(ListView):
    template_name = "base/list_page.html"
    context_object_name = "products"

    def get_queryset(self):
        #gets the most viewed products
        return TheProduct.objects.mostviewedproducts()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        context['user_profile'] = User.objects.get().profile
        return context
    
class MostRatedProducts(ListView):
    template_name = "base/list_page.html"
    context_object_name = "products"

    def get_queryset(self):
        return TheProduct.objects.mostratedproducts()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = page_pic.objects.get().website_pic
        context['user_profile'] = User.objects.get().profile
        return context