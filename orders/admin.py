"""
Admin configuration for orders app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items."""
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'get_subtotal']
    fields = ['product', 'product_name', 'quantity', 'price', 'get_subtotal']

    def get_subtotal(self, obj):
        if obj.id:
            return f"${obj.get_subtotal():.2f}"
        return "-"
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for Order model."""
    list_display = [
        'order_number',
        'user',
        'email',
        'total_amount',
        'status_badge',
        'created_at'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__email', 'email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'stripe_payment_intent_id']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('email', 'phone', 'shipping_address')
        }),
        ('Payment Information', {
            'fields': ('stripe_payment_intent_id',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    actions = ['mark_processing', 'mark_ready_for_pickup', 'mark_completed', 'mark_cancelled']

    def status_badge(self, obj):
        """Display status with colored badge."""
        colors = {
            'pending': 'yellow',
            'processing': 'blue',
            'ready_for_pickup': 'purple',
            'out_for_delivery': 'indigo',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def mark_processing(self, request, queryset):
        """Mark orders as processing."""
        queryset.update(status='processing')
        self.message_user(request, f'{queryset.count()} orders marked as processing.')
    mark_processing.short_description = 'Mark selected as Processing'

    def mark_ready_for_pickup(self, request, queryset):
        """Mark orders as ready for pickup."""
        queryset.update(status='ready_for_pickup')
        self.message_user(request, f'{queryset.count()} orders marked as ready for pickup.')
    mark_ready_for_pickup.short_description = 'Mark selected as Ready for Pickup'

    def mark_completed(self, request, queryset):
        """Mark orders as completed."""
        queryset.update(status='completed')
        self.message_user(request, f'{queryset.count()} orders marked as completed.')
    mark_completed.short_description = 'Mark selected as Completed'

    def mark_cancelled(self, request, queryset):
        """Mark orders as cancelled."""
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} orders marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected as Cancelled'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin for OrderItem model."""
    list_display = ['order', 'product_name', 'quantity', 'price', 'get_subtotal']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__order_number', 'product_name', 'product__name']
    readonly_fields = ['get_subtotal']

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'

