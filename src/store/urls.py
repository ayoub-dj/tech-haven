from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('login/',  views.login_view, name='login'),

    path('register/',  views.register_view, name='register'),

    path('logout/',  views.logout_view, name='logout'),

    path('cart/', views.cart_view, name='cart'),

    path('password-reset/', views.password_reset_view, name='password_reset'),

    path('password-reset/verify/<str:pk>/', views.password_reset_verify_view, name='password_reset_verify'),

    path('password-reset/done/<str:pk>/', views.password_reset_done_view, name='password_reset_done'),

    path('@<str:username>/',  views.profile_view, name='profile'),

    path('change-password-auth/<str:pk>/', views.change_password_auth_view, name='change_password_auth'),

    path('wishlist/', views.wishlist_view, name='wishlist'),

    path('product/<str:slug>/', views.single_product_view, name='single_product'),

    path('add/wishlist/<str:pk>', views.wishlist_handler, name='wishlist_handler'),

    path('<str:parent>/<str:slug>/products/', views.product_category_view, name='product_category'),

    path('add/review/<str:pk>', views.review_handler, name='review_handler'),

    path('remove-coupon-code/', views.remove_coupon_code, name='remove_coupon_code'),

    path('checkout/', views.checkout_view, name='checkout'),

]
