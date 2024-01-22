from django.urls import path
from django.contrib.auth import views
from .views import Home,HomeSearch,Product,NewArrivalsView,MostViewedProducts,MostRatedProducts

app_name = "base"

urlpatterns = [
    path('home',Home.as_view(),name="home"),
    path('home/search/',HomeSearch.as_view(),name="home_search"),
    path('product/<int:id>/',Product.as_view(),name="product"),
    path('newarrivals/',NewArrivalsView.as_view(),name="new_arrivals"),
    path('mostviewed/',MostViewedProducts.as_view(),name="most_viewed"),
    path('mostrated/',MostRatedProducts.as_view(),name="most_rated"),
]
