
from .models import *
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib import messages
import secrets
import json

User = get_user_model()


def header_handler():
    mobile_phones, mobile_phones_os, mobile_phones_hot_brand, computers, computers_appearance, computers_hot_brand, brands, brands_categories, accessories, accessories_categories, electronics, electronics_categories = None, None, None, None, None, None, None, None, None, None, None, None,

    try:
        # Start Mobile Phone Categories
        mobile_phones = Category.objects.get(category_slug="mobile-phones")
        mobile_phones_os = Category.objects.filter(parent=Category.objects.filter(parent=mobile_phones).get(category_slug="operating-system-mobile-phones"))
        mobile_phones_hot_brand = Category.objects.filter(parent=Category.objects.get(parent=mobile_phones, category_slug="hot-brands-mobile-phones"))
        # End Mobile Phone Categories

        # Start Computer Categories
        computers = Category.objects.get(category_slug="computers")
        computers_appearance = Category.objects.filter(parent=Category.objects.filter(parent=computers).get(category_slug="computer-appearance"))
        computers_hot_brand = Category.objects.filter(parent=Category.objects.get(parent=computers, category_slug="hot-brands-computer"))
        # End Computer Categories

        # Start Brand Categories
        brands  = Category.objects.get(category_slug="brands")
        brands_categories = Category.objects.filter(parent=brands)
        # Start Brand Categories

        # Start Accessories
        accessories = Category.objects.get(category_slug="accessories")
        accessories_categories = Category.objects.filter(parent=accessories)
        # End Accessories

        # Start Electronics
        electronics = Category.objects.get(category_slug="electronics")
        electronics_categories = Category.objects.filter(parent=electronics)
        # End Electronics
    except:
        pass
    
    return {
        'mobile_phones': mobile_phones,
        'mobile_phones_os': mobile_phones_os,
        'mobile_phones_hot_brand': mobile_phones_hot_brand,
        'computers': computers,
        'computers_appearance': computers_appearance,
        'computers_hot_brand': computers_hot_brand,
        'brands': brands,
        'brands_categories': brands_categories,
        'accessories': accessories,
        'accessories_categories': accessories_categories,
        'electronics': electronics,
        'electronics_categories': electronics_categories,
    }



def getCartCookie(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = None
        
    cart_items = []
    items_count = 0
    total_price = 0

    if cart is not None:
        for i in cart:
            try:
                product = Product.objects.get(pk=i)
                items_count += cart[i]['quantity']
                total_price += product.product_price * cart[i]['quantity']

                item = {
                    'product_id': product.id,
                    'product_name': product.product_name,
                    'product_price': product.product_price,
                    'product_image': product.product_main_image.url,
                    'product_quantity': cart[i]['quantity'],
                }
                cart_items.append(item)
            except:
                pass
    
    return {
        'cart_items': cart_items,
        'items_count': items_count,
        'total_price': total_price,
    }


def generate_secure_six_digit_number():
    number = secrets.randbelow(900000) + 100000
    return f"{number:06d}"


def send_six_digit_number_to_email(request, sixDigit, user_id):
    user = get_object_or_404(User, id=user_id)
    receiver = user.email
    email_subject = f'{sixDigit} is your TechHaven account recovery code'
    message = render_to_string('email_templates/password-reset-email.html', {
        'username': user.username,
        'code': sixDigit,
    })

    email = EmailMessage(
        subject=email_subject,
        body=message,
        to=[receiver]
    )

    try:
        email.send()
        messages.success(request, f'A verification code has been sent to your email address. ({receiver}) Please check your inbox or spam folder.')
    except Exception as e:
        messages.error(request, f'Oops! It seems there was a problem while trying to send your email ({receiver}). Please try again later or contact support for assistance.')


def create_unique_slug(name, target):
    slug = slugify(name)
    unique_slug = slug

    if target == 'product':
        number = 1
        while Product.objects.filter(product_slug=unique_slug).exists():
            unique_slug = f"{slug}-{number}"
            number += 1
            
    elif target == 'category':
        number = 1
        while Category.objects.filter(category_slug=unique_slug).exists():
            unique_slug = f"{slug}-{number}"
            number += 1

            
    return unique_slug

