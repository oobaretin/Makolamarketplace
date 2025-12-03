"""
Store models for Makola Marketplace.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsletterSubscriber(models.Model):
    """
    Newsletter subscription model.
    """
    email = models.EmailField(_('email'), unique=True)
    is_active = models.BooleanField(_('is active'), default=True)
    subscribed_at = models.DateTimeField(_('subscribed at'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('unsubscribed at'), null=True, blank=True)

    class Meta:
        verbose_name = _('newsletter subscriber')
        verbose_name_plural = _('newsletter subscribers')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

