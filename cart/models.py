"""
Cart models for Makola Marketplace.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    """
    Shopping cart model for logged-in users.
    """
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Cart for {self.user.email}"

    def get_total(self):
        """Calculate total cart value."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Individual item in shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('cart')
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price_at_addition = models.DecimalField(
        _('price at addition'),
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
        unique_together = ['cart', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"

    def get_subtotal(self):
        """Calculate subtotal for this item."""
        return self.price_at_addition * self.quantity

