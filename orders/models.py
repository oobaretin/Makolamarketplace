"""
Order models for Makola Marketplace.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class Order(models.Model):
    """
    Order model for customer purchases.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('ready_for_pickup', _('Ready for Pickup')),
        ('out_for_delivery', _('Out for Delivery')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('user')
    )
    order_number = models.CharField(_('order number'), max_length=20, unique=True)
    total_amount = models.DecimalField(
        _('total amount'),
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    shipping_address = models.TextField(_('shipping address'))
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'))
    stripe_payment_intent_id = models.CharField(
        _('stripe payment intent id'),
        max_length=255,
        blank=True
    )
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        while True:
            order_number = f"MK{get_random_string(8, '0123456789')}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def get_status_display_class(self):
        """Get CSS class for status badge."""
        status_classes = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'processing': 'bg-blue-100 text-blue-800',
            'ready_for_pickup': 'bg-purple-100 text-purple-800',
            'out_for_delivery': 'bg-indigo-100 text-indigo-800',
            'completed': 'bg-green-100 text-green-800',
            'cancelled': 'bg-red-100 text-red-800',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')


class OrderItem(models.Model):
    """
    Individual item in an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('product')
    )
    product_name = models.CharField(_('product name'), max_length=200)  # Store name in case product is deleted
    quantity = models.PositiveIntegerField(_('quantity'))
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order {self.order.order_number}"

    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.price * self.quantity

