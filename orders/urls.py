"""
URLs for orders app.
"""
from django.urls import path
from .views import shopping_list_view

app_name = 'orders'

urlpatterns = [
    path('shopping-list/', shopping_list_view, name='shopping_list'),
]







