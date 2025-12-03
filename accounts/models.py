"""
User account models for Makola Marketplace.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds additional fields for e-commerce functionality.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    address = models.CharField(_('street address'), max_length=255, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=50, blank=True, default='TX')
    zip_code = models.CharField(_('zip code'), max_length=10, blank=True)
    email_verified = models.BooleanField(_('email verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_address(self):
        """Return formatted full address."""
        parts = [self.address, self.city, self.state, self.zip_code]
        return ', '.join(filter(None, parts))


class EmailVerificationToken(models.Model):
    """
    Model to store email verification tokens.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('email verification token')
        verbose_name_plural = _('email verification tokens')
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification token for {self.user.email}"



