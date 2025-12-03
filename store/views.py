"""
Views for store app.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterSubscriber
from .forms import ContactForm, NewsletterForm


def about_view(request):
    """
    Display about page.
    """
    return render(request, 'store/about.html')


def contact_view(request):
    """
    Display contact page and handle contact form submissions.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['subject']}",
                message=f"From: {form.cleaned_data['name']} ({form.cleaned_data['email']})\n\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('store:contact')
    else:
        form = ContactForm()
    
    # Store location coordinates
    store_location = {
        'lat': 29.6556701,
        'lng': -95.5355849,
        'address': '9051 W Bellfort Ave, Houston, TX 77031',
        'phone': '(713) 995-4343'
    }
    
    context = {
        'form': form,
        'store_location': store_location,
    }
    
    return render(request, 'store/contact.html', context)


def newsletter_subscribe_view(request):
    """
    Handle newsletter subscription.
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if not created:
                if subscriber.is_active:
                    messages.info(request, 'You are already subscribed to our newsletter.')
                else:
                    subscriber.is_active = True
                    subscriber.unsubscribed_at = None
                    subscriber.save()
                    messages.success(request, 'You have been resubscribed to our newsletter!')
            else:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            
            return redirect('products:product_list')
    else:
        form = NewsletterForm()
    
    return render(request, 'store/newsletter.html', {'form': form})


def blog_cooked_food_view(request):
    """
    Display blog post about cooked food area.
    """
    return render(request, 'store/blog_cooked_food.html')


def blog_shopping_experience_view(request):
    """
    Display blog post about shopping experience.
    """
    return render(request, 'store/blog_shopping_experience.html')

