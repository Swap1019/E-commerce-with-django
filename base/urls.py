from django.urls import path
from django.contrib.auth import views
from .views import (
    HomeView,
    HomeSearchView,
    ProductView,
    NewArrivalsView,
    MostViewedProducts,
    MostRatedProducts,
    AddToCartView,
    IncreaseUpdateCartView,
    DecreaseUpdateCartView,
    UserCartView,
    UserCartDeleteView,
    UserCartCheckoutView,
    )
    

app_name = 'base'

urlpatterns = [
    path('home',HomeView.as_view(),name='home'),
    path('home/search/',HomeSearchView.as_view(),name='home_search'),
    path('product/<int:id>/',ProductView.as_view(),name='product'),
    path('addtocart/<int:id>/',AddToCartView.as_view(),name='add_to_cart'),
    path('increaseupdatecart/<int:id>/',IncreaseUpdateCartView.as_view(),name='increase_update_cart'),
    path('decreaseupdatecart/<int:id>/',DecreaseUpdateCartView.as_view(),name='decrease_update_cart'),
    path('cart/',UserCartView.as_view(),name='cart'),
    path('cart/delete/<int:id>',UserCartDeleteView.as_view(),name='cart_delete'),
    path('cart/checkout/',UserCartCheckoutView.as_view(),name='cart_checkout'),
    path('newarrivals/',NewArrivalsView.as_view(),name='new_arrivals'),
    path('mostviewed/',MostViewedProducts.as_view(),name='most_viewed'),
    path('mostrated/',MostRatedProducts.as_view(),name='most_rated'),
]
