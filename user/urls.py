from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    Register,
    UserLogin,
    UserLogout,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    AccountView,
    PurchasedProductsView,
    SellerRegisterFormView,
    NewSellerRequests,
    NewSellerRequestsSearch,
    SellerRequest,
    ShopTotalView,
    ShopMostViewedProductsView,
    ShopMostRatedProductsView,
    ShopNewArrivalProductsView,
    ShopUnavailableProductsView,
    ShopSearchView,
    AddProductView,
    ShippingProgressSellerView,
    ShippingStatusUpdateView,
    NewProductsView,
    NewProductsSearchView,
    NewProductApproveView,
    ProductReportsView,
    ReportedProductView,
    ProductDeleteView,
    )

app_name = "user"

urlpatterns = [
    #register and form urls
    path('register/',Register.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('seller-register/',SellerRegisterFormView.as_view(),name='seller_register'),
    path('new-seller-requests/',NewSellerRequests.as_view(),name='new_seller_requests'),
    path('new-seller-requests/search/',NewSellerRequestsSearch.as_view(),name='new_seller_requests_search'),
    path('seller-request/<uuid:user_id>',SellerRequest.as_view(),name='seller_request_detail'),
    path('profile/',AccountView.as_view(),name='profile'),
    path('purchased-products/',PurchasedProductsView.as_view(),name='purchased_products'),
    path('shop/',ShopTotalView.as_view(),name='shop'),
    path('shop/mostviewed',ShopMostViewedProductsView.as_view(),name='shop_mostviewed'),
    path('shop/mostrated',ShopMostRatedProductsView.as_view(),name='shop_mostrated'),
    path('shop/newarrivals',ShopNewArrivalProductsView.as_view(),name='shop_newarrivals'),
    path('shop/unavailables',ShopUnavailableProductsView.as_view(),name='shop_unavailables'),
    path('shop/search/',ShopSearchView.as_view(),name='shop_search'),
    path('shop/addproduct',AddProductView.as_view(),name='add_product'),
    path('shop/shipping-progress-seller',ShippingProgressSellerView.as_view(),name='shipping_progress_seller'),
    path('shop/shipping-progress-seller/update/<int:id>/<str:value>',ShippingStatusUpdateView.as_view(),name='shipping-status-update-view'),
    path('newproducts/',NewProductsView.as_view(),name='new_products'),
    path('newproducts/search/',NewProductsSearchView.as_view(),name='new_products_search'),
    path('newproducts/product/<int:id>',NewProductApproveView.as_view(),name='new_products_approve'),
    path('reportedproducts/',ProductReportsView.as_view(),name='product_reports'),
    path('reportedproducts/reportedproduct/<int:id>',ReportedProductView.as_view(),name='reported_product_view'),
    path('reportedproducts/reportedproduct/<int:id>/delete/',ProductDeleteView.as_view(),name='product_delete_view'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)