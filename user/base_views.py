from .models import ReportedProduct
from django.views.generic import (
    ListView,
    )

class BaseProductReportsView(ListView):
    template_name = 'user/reported_products_list.html'
    context_object_name = 'reported_products'

class BaseShopView(ListView):
    template_name = 'user/shop.html'
    context_object_name = 'created_products'