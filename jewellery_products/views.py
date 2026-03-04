from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Category, Product, Testimonial


# ─── Cart helpers ─────────────────────────────────────────

def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _cart_total(cart):
    return sum(float(item['price']) * item['quantity'] for item in cart.values())


def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_featured=True, in_stock=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def products(request):
    category_slug = request.GET.get('category')
    all_categories = Category.objects.all()
    products_qs = Product.objects.filter(in_stock=True)
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products_qs = products_qs.filter(category=active_category)

    context = {
        'products': products_qs,
        'categories': all_categories,
        'active_category': active_category,
    }
    return render(request, 'products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category, in_stock=True).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related,
    }
    return render(request, 'product_detail.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            messages.success(request, "Thank you for reaching out! We'll get back to you within 24 hours.")
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'contact.html')


# ─── Cart views ───────────────────────────────────────────

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    key = str(product_id)
    qty = int(request.POST.get('quantity', 1))

    if key in cart:
        cart[key]['quantity'] = min(cart[key]['quantity'] + qty, 10)
    else:
        cart[key] = {
            'name': product.name,
            'price': float(product.display_price),
            'original_price': float(product.price),
            'image': product.image.url if product.image else '',
            'slug': product.slug,
            'category': product.category.name,
            'quantity': qty,
        }

    _save_cart(request, cart)
    cart_count = sum(i['quantity'] for i in cart.values())

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': f'"{product.name}" added to your bag!',
        })
    return redirect('cart_detail')


@require_POST
def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    return redirect('cart_detail')


@require_POST
def update_cart(request, product_id):
    cart = _get_cart(request)
    key = str(product_id)
    qty = int(request.POST.get('quantity', 1))
    if key in cart:
        if qty < 1:
            cart.pop(key)
        else:
            cart[key]['quantity'] = min(qty, 10)
    _save_cart(request, cart)
    return redirect('cart_detail')


def cart_detail(request):
    cart = _get_cart(request)
    subtotal = _cart_total(cart)
    shipping = 0 if subtotal >= 2999 else 199
    total = subtotal + shipping
    context = {
        'cart': cart,
        'cart_items': list(cart.items()),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'cart_count': sum(i['quantity'] for i in cart.values()),
    }
    return render(request, 'cart.html', context)
