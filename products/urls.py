"""
URLs for products app.
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('product/<slug:slug>/review/', views.add_review_view, name='add_review'),
]

