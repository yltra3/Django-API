from django.urls import path

from . import views

urlpatterns = [
    path(r'first/', views.first),
    path(r'second/', views.second),
]