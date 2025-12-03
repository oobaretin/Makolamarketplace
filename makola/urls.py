"""
URL configuration for Makola Marketplace project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('store/', include('store.urls')),
]

# Serve media files in development
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# Customize admin site
admin.site.site_header = "Makola Marketplace Administration"
admin.site.site_title = "Makola Marketplace Admin"
admin.site.index_title = "Welcome to Makola Marketplace Administration"

