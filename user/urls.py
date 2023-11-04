from django.urls import path
from .views import (
    Register,
    UserLogin,
    UserLogout,
    AccountView,
    SellerRegisterFormView,
    NewSellerRequests,
    SellerRequest,
    )

urlpatterns = [
    path('register/',Register.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('profile/',AccountView.as_view(),name='profile'),
    path('seller-register/',SellerRegisterFormView.as_view(),name='seller-register'),
    path('new-seller-requests/',NewSellerRequests.as_view(),name='new-seller-requests'),
    path('seller-request/<uuid:user_id>',SellerRequest.as_view(),name='seller-request-detail')
]