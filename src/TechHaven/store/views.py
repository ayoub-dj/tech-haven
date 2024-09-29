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


# Start Login View
def login_view(request):
    items_count = getCartCookie(request)['items_count']

    try:
        wishlist = WishList.objects.filter(customer_wishlist=request.user.customer)
        wishlist_count = wishlist.count()
    except:
        wishlist = None
        wishlist_count = None

    # Start Start Header Handler
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
    # End Start Header Handler

    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your successful Logged in  Welcome Back :) !")
                if request.GET.get('next'): return redirect(request.GET.get('next'))
                else: return redirect('home')

    else:  form = LoginForm()

    context = {
        'form': form,

        'items_count': items_count,

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

    }
    return render(request, 'login.html', context)
# End Login View


# Start Register View
def register_view(request):
    items_count = getCartCookie(request)['items_count']

    try:
        wishlist = WishList.objects.filter(customer_wishlist=request.user.customer)
        wishlist_count = wishlist.count()
    except:
        wishlist = None
        wishlist_count = None

    # Start Start Header Handler
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
    # End Start Header Handler

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            try:
                user = User(email=email, username=username)
                user.set_password(password)
                
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                user = authenticate(request, email=email, password=password)
            except:
                user = None

            customer = form.save(commit=False)

            if user is not None:
                customer.user = user
                customer.save()
                login(request, user)
                messages.success(request, "Your registration was successful—thank you for choosing us !")
                return redirect('home')
            
    else: form = CustomerForm()

    context = {
        'form': form,

        'items_count': items_count,
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

    }
    return render(request, 'register.html', context)
# End Register View


# Start Logout View
@login_required(login_url='login')
def logout_view(request):
    logout(request)

    return redirect('login')
# End Logout View

# Start Cart View
def cart_view(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            request.session['code'] = code
    else:
        form = CouponForm()


    try:
        wishlist = WishList.objects.filter(customer_wishlist=request.user.customer)
        wishlist_count = wishlist.count()
    except:
        wishlist = None
        wishlist_count = 0

    code = request.session.get('code', None)

    if request.session.get('code'):
        coupon = Coupon.objects.get(code=code)
        total_price = coupon.apply_discount(getCartCookie(request)['total_price'])
    else:
        total_price = getCartCookie(request)['total_price']

    cart_items = getCartCookie(request)['cart_items']
    items_count = getCartCookie(request)['items_count']

    # Start Start Header Handler
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
    # End Start Header Handler
    


    context = {
        'cart_items': cart_items,

        'wishlist_count': wishlist_count,

        'items_count': items_count,
        
        'total_price': total_price,

        'form': form,

        'code': code,

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
    }

    return render(request, 'cart.html', context)
# End Cart View

