from django.urls import path
from django.contrib.auth import views
from .views import (
    Home,
    HomeSearch,
    Product,
    NewArrivalsView,
    MostViewedProducts,
    MostRatedProducts,
    AddToCartView,
    IncreaseUpdateCartView,
    DecreaseUpdateCartView,
    UserCartView,
    UserCartDeleteView,
    )
    

app_name = 'base'

urlpatterns = [
    path('home',Home.as_view(),name='home'),
    path('home/search/',HomeSearch.as_view(),name='home_search'),
    path('product/<int:id>/',Product.as_view(),name='product'),
    path('addtocart/<int:id>/',AddToCartView.as_view(),name='add_to_cart'),
    path('increaseupdatecart/<int:id>/',IncreaseUpdateCartView.as_view(),name='increase_update_cart'),
    path('decreaseupdatecart/<int:id>/',DecreaseUpdateCartView.as_view(),name='decrease_update_cart'),
    path('cart/',UserCartView.as_view(),name='cart'),
    path('cart/delete/<int:id>',UserCartDeleteView.as_view(),name='cart_delete'),
    path('newarrivals/',NewArrivalsView.as_view(),name='new_arrivals'),
    path('mostviewed/',MostViewedProducts.as_view(),name='most_viewed'),
    path('mostrated/',MostRatedProducts.as_view(),name='most_rated'),
]
