"""
URLs for store app.
"""
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('newsletter/', views.newsletter_subscribe_view, name='newsletter'),
    path('blog/cooked-food/', views.blog_cooked_food_view, name='blog_cooked_food'),
    path('blog/shopping-experience/', views.blog_shopping_experience_view, name='blog_shopping_experience'),
]

