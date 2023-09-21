from django.urls import path
from django.contrib.auth import views
from .views import home

app_name = "base"

urlpatterns = [
    path('',home.as_view(),name="home")
]
