from django.contrib import admin
from .models import Category, Product, Testimonial, Order, OrderItem


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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'name', 'price', 'quantity', 'image', 'line_total']
    fields = ['product', 'name', 'price', 'quantity', 'line_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'phone', 'total',
                    'payment_method', 'payment_status', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['order_number', 'razorpay_order_id', 'razorpay_payment_id', 'created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
