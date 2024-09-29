from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import (
    CustomerForm,
    LoginForm,
    ProfileFormCustomer,
    CustomPasswordResetFormDone,
    CustomPasswordResetForm,
    SixDigitForm,
    CouponForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Customer,
    Product,
    Category,
    Review,
    PasswordResetCode,
    WishList,
    Coupon,
)
from django.http import HttpResponse
from .utils import (
    header_handler,
    generate_secure_six_digit_number,
    send_six_digit_number_to_email,
    getCartCookie,
)
User = get_user_model()

# Start Home View
def home_view(request):
    items_count = getCartCookie(request)['items_count']

    try:
        wishlist = WishList.objects.filter(customer_wishlist=request.user.customer)
        wishlist_count = wishlist.count()
    except:
        wishlist = None
        wishlist_count = None

    mobile_phones = header_handler()['mobile_phones']
    mobile_phones_os = header_handler()['mobile_phones_os']
    mobile_phones_hot_brand = header_handler()['mobile_phones_hot_brand']

    computers = header_handler()['computers']
    computers_appearance = header_handler()['computers_appearance']
    computers_hot_brand = header_handler()['computers_hot_brand']

    brands  = header_handler()['brands']
    brands_categories = header_handler()['brands_categories']

    accessories = header_handler()['accessories']
    accessories_categories = header_handler()['accessories_categories']

    electronics = header_handler()['electronics']
    electronics_categories = header_handler()['electronics_categories']

    products = Product.objects.all()

    reviews = [i for i in Review.objects.all() if i.score >= 4.0]


    context = {
        'products': products,

        # 'items_count': items_count,
        'wishlist_count': wishlist_count,

        # Start Header Handler
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
        # End Header Handler

        'reviews': reviews,
    }
    
    return render(request, 'index.html', context)
# End Home View
