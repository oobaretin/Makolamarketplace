"""
Admin configuration for products app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model."""
    list_display = ['name', 'slug', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        """Display number of products in category."""
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model."""
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'country_of_origin', 'created_at']
    search_fields = ['name', 'description', 'country_of_origin']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'product_image_preview']
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity', 'is_available')
        }),
        ('Additional Information', {
            'fields': ('country_of_origin', 'image', 'product_image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_image_preview(self, obj):
        """Display product image preview in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "No image"
    product_image_preview.short_description = 'Image Preview'

    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        """Admin action to make products available."""
        queryset.update(is_available=True)
        self.message_user(request, f'{queryset.count()} products marked as available.')
    make_available.short_description = 'Mark selected products as available'

    def make_unavailable(self, request, queryset):
        """Admin action to make products unavailable."""
        queryset.update(is_available=False)
        self.message_user(request, f'{queryset.count()} products marked as unavailable.')
    make_unavailable.short_description = 'Mark selected products as unavailable'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin for ProductImage model."""
    list_display = ['product', 'is_primary', 'image_preview', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
    readonly_fields = ['created_at', 'image_preview']

    def image_preview(self, obj):
        """Display image preview in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin for Review model."""
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__email', 'comment']
    readonly_fields = ['created_at', 'updated_at']



