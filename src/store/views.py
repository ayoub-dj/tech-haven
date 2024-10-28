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
from django.http import HttpResponse

from .models import *
from django.http import HttpResponse
from .utils import *

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

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


# Start Password Reset
def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = get_object_or_404(User, email=email)
            code = generate_secure_six_digit_number()
            send_six_digit_number_to_email(request, code, user.id)
            reset_code = PasswordResetCode.objects.create(user=user, code=code)
            reset_code.save()

            return redirect('password_reset_verify', pk=user.id)

    else: form = CustomPasswordResetForm()

    context = {
        'form': form,
    }

    return render(request, 'password-reset.html', context)
# End Password Reset


# Start Password Reset Verify
def password_reset_verify_view(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        form = SixDigitForm(request.POST)

        if form.is_valid():
            six_digit_number = form.cleaned_data.get('six_digit_number')
            
            try:
                right_code = get_object_or_404(PasswordResetCode, user=user, code=six_digit_number)
                if right_code.is_expired():
                    messages.error(request, 'Reset code has expired.')
                    right_code.delete()
                else:
                    right_code.delete()
                    return redirect('password_reset_done', pk=user.id)
                

            except:
                messages.info(request, 'The verification code is not correct.')


    else: form = SixDigitForm()

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'password-reset-verify.html', context)
# End Password Reset Verify


# Start Password Reset Done
def password_reset_done_view(request, pk):
    user = get_object_or_404(User, id=pk)

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
        form = CustomPasswordResetFormDone(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password', None)
            if password is not None:
                user.set_password(raw_password=password)
                user.save()
                messages.success(request, 'Your Password has been changed successfully')
                user_done = authenticate(request, username=user.email, password=password)

                if user_done is not None:
                    login(request, user_done)
                    return redirect('home')
            
    else: form = CustomPasswordResetFormDone()

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
    return render(request, 'password-reset-done.html', context)
# End Password Reset Done


# Start Profile View
@login_required(login_url='login')
def profile_view(request, username):
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

    if request.user.id == User.objects.get(username=username).id:
        customer = Customer.objects.get(user=User.objects.get(username=username))
        if request.method == 'POST':
            profile_form = ProfileFormCustomer(instance=customer, data=request.POST, files=request.FILES, user=request.user)

            if profile_form.is_valid(): 
                avatar = request.FILES.get('avatar-image')
                user = User.objects.get(username=username)
                username_form = profile_form.cleaned_data['username']
                email_form = profile_form.cleaned_data['email']

                if username_form:
                    user.username = username_form

                if email_form:
                    user.email = email_form                

                if avatar is not None:
                    customer.avatar = avatar

                profile_form.save()
                user.save()

                messages.success(request, 'Profile Updated successfully')

                return redirect('profile', username=user.username)

            
        else:
            profile_form = ProfileFormCustomer(instance=customer, user=request.user)

        context = {
            'profile_form': profile_form,

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

        return render(request, 'profile.html', context)
    else:
        return HttpResponse('Not Allowed')
# End Profile View

# Start Change Password Auth
@login_required(login_url='login')
def change_password_auth_view(request, pk):
    user = User.objects.get(id=pk)
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password', None)
        password1 = request.POST.get('new_password1', None)
        password2 = request.POST.get('new_password2', None)
        if user.check_password(old_password):
            if password1 and password2 and password1 == password2:
                user.set_password(raw_password=password1)
                user.save()
                messages.success(request, 'password successfully changed')
            else:
                messages.info(request, 'Passwords dont not match')
        else:
            messages.info(request, 'Old password does not correct')

    return redirect('profile', username=user.username)
# End Change Password Auth


# Start Single Product
def single_product_view(request, slug):
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

    product = get_object_or_404(Product, product_slug=slug)
    product_colors = product.product_colors.all()
    product_reviews = product.review_set.all()

    network_features, launch_details, body_details, display_details, platform_details, memory_details = None, None, None, None, None, None
    sound_features, communication_features, battery_details, main_camera_details, selfie_camera_details = None, None, None, None, None

    if hasattr(product, 'networkfeatures'):
        network_features = product.networkfeatures

    if hasattr(product, 'launchdetails'):
        launch_details = product.launchdetails

    if hasattr(product, 'bodydetails'):
        body_details = product.bodydetails

    if hasattr(product, 'displaydetails'):
        display_details = product.displaydetails

    if hasattr(product, 'platformdetails'):
        platform_details = product.platformdetails

    if hasattr(product, 'memorydetails'):
        memory_details = product.memorydetails
        
    if hasattr(product, 'soundfeatures'):
        sound_features = product.soundfeatures

    if hasattr(product, 'communicationfeatures'):
        communication_features = product.communicationfeatures

    if hasattr(product, 'batterydetails'):
        battery_details = product.batterydetails

    if hasattr(product, 'maincameradetails'):
        main_camera_details = product.maincameradetails

    if hasattr(product, 'selfiecameradetails'):
        selfie_camera_details = product.selfiecameradetails

    all_related_to_product = any([network_features, launch_details, body_details, display_details, platform_details, memory_details, sound_features, communication_features, battery_details, main_camera_details, selfie_camera_details])


    context = {
        'product': product,
        'product_colors': product_colors,
        'product_reviews': product_reviews,

        'items_count': items_count,
        'wishlist_count': wishlist_count,

        'all_related_to_product': all_related_to_product,

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

    return render(request, 'product-view.html', context)
# End Single Product


# Start WishList View
@login_required(login_url='login')
def wishlist_view(request):
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

    try:
        wishlist = WishList.objects.filter(customer_wishlist=request.user.customer)
        wishlist_count = wishlist.count()
    except:
        wishlist = None
        wishlist_count = None

    context = {
        'items_count': items_count,

        'wishlist': wishlist,
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

    return render(request, 'wishlist.html',  context)
# End WishList View


# Start WishList Handler
@login_required(login_url='login')
def wishlist_handler(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        customer = request.user.customer

        if not WishList.objects.filter(product=product, customer_wishlist=customer).exists():
            WishList.objects.create(product=product, customer_wishlist=customer)


        return redirect('single_product', slug=product.product_slug)
# End WishList Handler


# Start Remove Coupon Code
def remove_coupon_code(request):
    if request.method == 'POST':
        if 'code' in request.session:
            del request.session['code']
        return redirect('cart')
# End Remove Coupon Code


# Start Product Category
def product_category_view(request, parent, slug):
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


    child_category = Category.objects.get(category_slug=slug)
    category_products = child_category.products.all()
    category_products_count = category_products.count()


    context = {
        'products': category_products,
        'category_products_count': category_products_count,
        'child_category': child_category,

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

    return render(request, 'products.html', context)
# End Product Category


# Start Review Handler
@login_required(login_url='login')
def review_handler(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        customer = request.user.customer
        text = request.POST.get('content', None)
        rating = request.POST.get('rating', None)

        if Review.objects.filter(product=product, reviewer=customer).exists():
            messages.info(request, "You can't review product twice")
            return redirect('single_product', slug=product.product_slug)

        else:
            review = Review.objects.create(
                reviewer=customer,
                content=text,
                score=rating,
                product=product,
            )
            review.save()
            return redirect('single_product', slug=product.product_slug)
# End Review Handler


# Start Checkout
def checkout_view(request):
    items_count = getCartCookie(request)['items_count']
    total_price = getCartCookie(request)['total_price']
    cart_items = getCartCookie(request)['cart_items']

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

                
    # if request.method == 'POST':
    #     country = request.POST.get('country', None)
    #     house_number = request.POST.get('house_number', None)
    #     address = request.POST.get('address', None)
    #     city = request.POST.get('city', None)
    #     zipcode = request.POST.get('zipcode', None)

    #     shipping_address = ShippingAddress.objects.create(
    #         country=country,
    #         house_number=house_number,
    #         address=address,
    #         city=city,
    #         zipcode=zipcode,
    #     )

    #     if request.user.is_authenticated:
    #         customer = request.user.customer
    #         name = f"{request.user.customer.first_name} {request.user.customer.last_name}"
    #         email = request.user.email

    #         shipping_address.customer = customer
    #         shipping_address.save()

    #         Order.objects.create(
    #             customer=customer,
    #             name=name,
    #             email=email,
    #             shipping_address=shipping_address,
    #         )

    #         return HttpResponse('Authenticated User')
            
    #     else:
    #         name = request.POST.get('name', None)
    #         email = request.POST.get('email', None)

    #         Order.objects.create(
    #             name=name,
    #             email=email,
    #             customer=customer,
    #         )

    #         return HttpResponse('Guest User')



    context = {
        'items_count': items_count,
        'total_price': total_price,
        'cart_items': cart_items,

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

    return render(request, 'checkout.html', context)
# End Checkout

from django.http import JsonResponse

def process_order(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        house_number = request.POST.get('house_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        if not request.user.is_authenticated:
            name = request.POST.get('name')
            email = request.POST.get('email')
            order = Order.objects.create(
                email=email,
                name=name,
            )
            shipping_address = ShippingAddress.objects.create(
                order=order,
                country=country,
                house_number=house_number,
                address=address,
                city=city,
                zipcode=zipcode
            )
            cookie = getCartCookie(request)['cart_items']
            for i in cookie:
                product_id = int(i['product_id'])
                product_quantity = int(i['product_quantity'])

                product = get_object_or_404(Product, pk=product_id)
                OrderItems.objects.create(
                    order=order,
                    product=product,
                    quantity=product_quantity,
                )
        else:
            customer = request.user.customer
            name = request.user.username
            email = request.user.email
            order = Order.objects.create(
                customer=customer,
                email=email,
                name=name,
            )
            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                country=country,
                house_number=house_number,
                address=address,
                city=city,
                zipcode=zipcode
            )
            cookie = getCartCookie(request)['cart_items']
            for i in cookie:
                product_id = int(i['product_id'])
                product_quantity = int(i['product_quantity'])
                product = get_object_or_404(Product, pk=product_id)
                OrderItems.objects.create(
                    order=order,
                    product=product,
                    quantity=product_quantity,
                )
        checkout_session = stripe.checkout.Session.create(
            customer_email = email,
            payment_method_types = ['card'],
            line_items = [
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                            'name': 'simple',
                        },
                        'unit_amount': int(order.total_price()) * 100,
                    },
                    'quantity': 1
                }
            ],
            mode = 'payment',
            success_url='https://google.com',
            cancel_url='https://facebook.com'
        )
        return redirect(checkout_session.url)