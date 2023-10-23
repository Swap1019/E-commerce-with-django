from django.urls import path
from .views import Register,UserLogin,UserLogout,AccountView

urlpatterns = [
    path('register/',Register.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',UserLogout.as_view(),name='logout'),
    path('profile/',AccountView.as_view(),name='profile'),
]