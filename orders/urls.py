"""
URLs for orders app.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment-success/<str:order_number>/', views.payment_success_view, name='payment_success'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('', views.order_list_view, name='order_list'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]

