"""
Views for accounts app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm, UserProfileForm
from .models import User, EmailVerificationToken


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create email verification token
            token = get_random_string(64)
            EmailVerificationToken.objects.create(user=user, token=token)
            
            # Send verification email
            verification_url = f"{settings.SITE_URL}/accounts/verify-email/{token}/"
            send_mail(
                'Verify your email - Makola Marketplace',
                f'Please click the following link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request, token):
    """Handle email verification."""
    try:
        verification = EmailVerificationToken.objects.get(token=token, is_used=False)
        verification.user.email_verified = True
        verification.user.save()
        verification.is_used = True
        verification.save()
        messages.success(request, 'Email verified successfully! You can now log in.')
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid or expired verification token.')
    
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Display and update user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def order_history_view(request):
    """Display user's order history."""
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/order_history.html', {'orders': orders})



