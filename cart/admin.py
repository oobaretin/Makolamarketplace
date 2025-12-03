"""
Admin configuration for cart app.
"""
from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items."""
    model = CartItem
    extra = 0
    readonly_fields = ['price_at_addition', 'created_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin for Cart model."""
    list_display = ['user', 'get_item_count', 'get_total', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]

    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'

    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin for CartItem model."""
    list_display = ['cart', 'product', 'quantity', 'price_at_addition', 'get_subtotal', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['cart__user__email', 'product__name']
    readonly_fields = ['price_at_addition', 'created_at', 'updated_at']

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'



