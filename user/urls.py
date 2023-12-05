from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    Register,
    UserLogin,
    AccountView,
    SellerRegisterFormView,
    NewSellerRequests,
    SellerRequest,
    ShopTotalView,
    ShopMostViewedProductsView,
    ShopMostRatedProductsView,
    ShopNewArrivalProductsView,
    ShopUnavailableProductsView,
    )

app_name = "user"

urlpatterns = [
    #register and form urls
    path('register/',Register.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('seller-register/',SellerRegisterFormView.as_view(),name='seller-register'),
    path('new-seller-requests/',NewSellerRequests.as_view(),name='new-seller-requests'),
    path('seller-request/<uuid:user_id>',SellerRequest.as_view(),name='seller-request-detail'),
    #user interface urls
    path('profile/',AccountView.as_view(),name='profile'),
    path('shop/',ShopTotalView.as_view(),name='shop'),
    path('shop/mostviewed',ShopMostViewedProductsView.as_view(),name='shop_mostviewed'),
    path('shop/mostrated',ShopMostRatedProductsView.as_view(),name='shop_mostrated'),
    path('shop/newarrivals',ShopNewArrivalProductsView.as_view(),name='shop_newarrivals'),
    path('shop/unavailables',ShopUnavailableProductsView.as_view(),name='shop_unavailables'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)