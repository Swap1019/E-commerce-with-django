from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from .views import (
    Register,
    UserLogin,
    UserLogout,
    AccountView,
    SellerRegisterFormView,
    NewSellerRequests,
    NewSellerRequestsSearch,
    SellerRequest,
    ShopTotalView,
    ShopMostViewedProductsView,
    ShopMostRatedProductsView,
    ShopNewArrivalProductsView,
    ShopUnavailableProductsView,
    ShopSearch,
    AddProduct,
    NewProducts,
    NewProductsSearch,
    NewProductApprove,
    )

app_name = "user"

urlpatterns = [
    #register and form urls
    path('register/',Register.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('seller-register/',SellerRegisterFormView.as_view(),name='seller_register'),
    path('new-seller-requests/',NewSellerRequests.as_view(),name='new_seller_requests'),
    path('new-seller-requests/search/',NewSellerRequestsSearch.as_view(),name='new_seller_requests_search'),
    path('seller-request/<uuid:user_id>',SellerRequest.as_view(),name='seller_request_detail'),
    #user interface urls
    path('profile/',AccountView.as_view(),name='profile'),
    path('shop/',ShopTotalView.as_view(),name='shop'),
    path('shop/mostviewed',ShopMostViewedProductsView.as_view(),name='shop_mostviewed'),
    path('shop/mostrated',ShopMostRatedProductsView.as_view(),name='shop_mostrated'),
    path('shop/newarrivals',ShopNewArrivalProductsView.as_view(),name='shop_newarrivals'),
    path('shop/unavailables',ShopUnavailableProductsView.as_view(),name='shop_unavailables'),
    path('shop/search/',ShopSearch.as_view(),name='shop_search'),
    path('shop/addproduct',AddProduct.as_view(),name='add_product'),
    path('newproducts/',NewProducts.as_view(),name='new_products'),
    path('newproducts/search/',NewProductsSearch.as_view(),name='new_products_search'),
    path('newproducts/product/<int:id>',NewProductApprove.as_view(),name='new_products_approve'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)