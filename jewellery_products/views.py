import hmac
import hashlib

import razorpay
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Category, Product, Testimonial, Order, OrderItem


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


# ─── Checkout ─────────────────────────────────────────────

INDIAN_STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra & Nagar Haveli and Daman & Diu',
    'Delhi', 'Jammu & Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry',
]


def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.info(request, 'Your bag is empty.')
        return redirect('cart_detail')

    subtotal = _cart_total(cart)
    shipping = 0 if subtotal >= 2999 else 199
    total = subtotal + shipping

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        if not all([first_name, last_name, email, phone, address_line1, city, state, pincode]):
            messages.error(request, 'Please fill in all required fields.')
            context = {
                'cart_items': list(cart.items()), 'subtotal': subtotal,
                'shipping': shipping, 'total': total,
                'states': INDIAN_STATES, 'form_data': request.POST,
            }
            return render(request, 'checkout.html', context)

        order = Order.objects.create(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone,
            address_line1=address_line1, address_line2=address_line2,
            city=city, state=state, pincode=pincode,
            payment_method=payment_method,
            subtotal=subtotal, shipping_charge=shipping, total=total,
        )

        for key, item in cart.items():
            try:
                product = Product.objects.get(id=int(key))
            except Product.DoesNotExist:
                product = None
            OrderItem.objects.create(
                order=order, product=product,
                name=item['name'], price=item['price'],
                quantity=item['quantity'], image=item.get('image', ''),
            )

        if payment_method == 'cod':
            order.status = 'confirmed'
            order.save()
            _save_cart(request, {})
            return redirect('order_success', order_number=order.order_number)

        # Online – create Razorpay order
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        rz_order = client.order.create({
            'amount': int(float(total) * 100),
            'currency': 'INR',
            'receipt': order.order_number,
        })
        order.razorpay_order_id = rz_order['id']
        order.save()

        return render(request, 'payment.html', {
            'order': order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': rz_order['id'],
            'amount_paise': int(float(total) * 100),
            'amount_display': total,
        })

    context = {
        'cart_items': list(cart.items()),
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'states': INDIAN_STATES,
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
def payment_callback(request):
    if request.method != 'POST':
        return redirect('home')

    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')

    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('cart_detail')

    # Verify signature
    msg = f'{razorpay_order_id}|{razorpay_payment_id}'.encode()
    expected = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(), msg, hashlib.sha256
    ).hexdigest()  # noqa: hmac.new is the correct stdlib function

    if hmac.compare_digest(expected, razorpay_signature):
        order.razorpay_payment_id = razorpay_payment_id
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()
        _save_cart(request, {})
        return redirect('order_success', order_number=order.order_number)
    else:
        order.payment_status = 'failed'
        order.save()
        messages.error(request, 'Payment verification failed. Please contact support.')
        return redirect('cart_detail')


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'order_success.html', {'order': order})
