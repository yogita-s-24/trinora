from django.contrib import admin
from .models import Category, Product, Testimonial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'sale_price', 'is_featured', 'in_stock', 'created_at']
    list_filter = ['category', 'is_featured', 'in_stock']
    list_editable = ['is_featured', 'in_stock']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'is_active']
    list_editable = ['is_active']
    list_filter = ['rating', 'is_active']
