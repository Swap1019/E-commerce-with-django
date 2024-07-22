from .models import TheProduct
from django.views.generic import ListView

class BaseShopView(ListView):
    template_name = 'base/list_page.html'
    context_object_name = 'products'