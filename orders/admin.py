"""
Admin configuration for orders app.
"""
from django.contrib import admin
from django.utils.html import format_html
# from .models import Order, OrderItem


# class OrderItemInline(admin.TabularInline):
#     """Inline admin for order items (DISABLED)"""
#     model = OrderItem
#     extra = 0
#     readonly_fields = ('product', 'quantity', 'price_at_addition', 'subtotal')
#     fields = ('product', 'quantity', 'price_at_addition', 'subtotal')
#
#     def subtotal(self, obj):
#         return obj.price_at_addition * obj.quantity
#     subtotal.short_description = 'Subtotal'
#
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at')
#     list_filter = ('status', 'created_at')
#     search_fields = ('order_number', 'user__email', 'user__first_name', 'user__last_name', 'shipping_address', 'email', 'phone')
#     readonly_fields = ('order_number', 'total_amount', 'created_at', 'updated_at')
#     inlines = [OrderItemInline]
#     fieldsets = (
#         (None, {
#             'fields': ('order_number', 'user', 'total_amount', 'status', 'shipping_address', 'phone', 'email', 'created_at', 'updated_at', 'notes')
#         }),
#     )
# admin.site.register(Order, OrderAdmin)







