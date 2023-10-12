from django.urls import path
from django.contrib.auth import views
from .views import home,product,NewArrivalsView,MostViewedProducts

app_name = "base"

urlpatterns = [
    path('',home.as_view(),name="home"),
    path('product/<int:id>',product.as_view(),name="product"),
    path('newarrivals/',NewArrivalsView.as_view(),name="newarrivals"),
    path('mostviewed/',MostViewedProducts.as_view(),name="mostviewed"),
]
