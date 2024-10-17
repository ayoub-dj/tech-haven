from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Customer(models.Model):
    GENDER_CHOICES = [('M', 'male'), ('F', 'female')]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20)
    house_number = models.IntegerField()
    city = models.CharField(max_length=100)
    country = CountryField(blank_label='Select country', default='US')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    joined = models.DateTimeField(auto_now_add=True)

    @property
    def get_username(self):
        return self.user.username

    def __str__(self):
        return f"{self.user}"
    
    class Meta:
        ordering = ('-joined', )


class NetworkFeatures(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='network_features')
    technology = models.CharField(max_length=255, null=True, blank=True)
    two_g_bands = models.CharField(max_length=255, null=True, blank=True)
    three_g_bands = models.CharField(max_length=255, null=True, blank=True)
    speed = models.CharField(max_length=255, null=True, blank=True)
    four_bands = models.CharField(max_length=255, null=True, blank=True)
    five_g_bands = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Network: {self.product.product_name}, "


class LaunchDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    announced = models.DateField()
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Announced: {self.announced}, Status: {self.status}"


class BodyDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    dimensions = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    build = models.CharField(max_length=255, null=True, blank=True)
    sim = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Dimensions: {self.dimensions}, Weight: {self.weight}g"


class DisplayDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    display_type = models.CharField(max_length=255, null=True, blank=True)
    display_size = models.CharField(max_length=255, null=True, blank=True)
    display_resolution = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Type: {self.display_type}, Size: {self.display_size}"


class PlatformDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    chipset = models.CharField(max_length=255, null=True, blank=True)
    cpu = models.CharField(max_length=255, null=True, blank=True)
    gpu = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"OS: {self.os}, Chipset: {self.chipset}"


class MemoryDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    memory_card_slot = models.BooleanField()
    ram = models.CharField(max_length=255, null=True, blank=True)
    storage = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"MemoryDetails: {self.memory_card_slot}"


class SoundFeatures(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    loudspeaker = models.CharField(max_length=255, null=True, blank=True)
    jack_3_5mm = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"SoundFeatures"


class CommunicationFeatures(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    wlan = models.CharField(max_length=255, null=True, blank=True)
    bluetooth = models.CharField(max_length=255, null=True, blank=True)
    radio = models.CharField(max_length=255, null=True, blank=True)
    usb = models.CharField(max_length=255, null=True, blank=True)
    nfc = models.CharField(max_length=255, null=True, blank=True)
    comms = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"WLAN: {self.wlan}"


class BatteryDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    battery_type = models.CharField(max_length=355, null=True, blank=True)
    Charging = models.CharField(max_length=355, null=True, blank=True)

    def __str__(self):
        return f"Battery: {self.battery_type}"


class MainCameraDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    main_camera_features = models.CharField(max_length=255, null=True, blank=True)
    main_camera_video = models.CharField(max_length=255, null=True, blank=True)
    main_camera_dual = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Main Camera: {self.main_camera_features}"


class SelfieCameraDetails(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    selfie_camera_single = models.CharField(max_length=255, null=True, blank=True)
    selfie_camera_features = models.CharField(max_length=255, null=True, blank=True)
    selfie_camera_video = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Selfie Camera: {self.selfie_camera_features}"


class PackageContent(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    includes = models.TextField(null=True, blank=True)

class VideoReview(models.Model):
    product = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True, blank=True)
    frame_link = models.CharField(max_length=500, null=True, blank=True)
    video = models.FileField(upload_to='video_reviews/', null=True, blank=True)

class Product(models.Model):
    product_name = models.CharField(max_length=333)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_main_image = models.ImageField(upload_to="product_main_image/", null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    total_rating = models.PositiveIntegerField(default=0)
    product_slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='products')

    def update_rating(self):
        ratings = self.review_set.aggregate(
            average_ratings=Avg('score'),
            total_ratings=Count('id')
        )
        self.average_rating = ratings['average_ratings'] or 0.0
        self.total_rating = ratings['total_ratings'] or 0
        self.save()

    def __str__(self):
        return f"{self.product_name}"


class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='product_colors', on_delete=models.CASCADE)
    color_name = models.CharField(max_length=50)
    color_hex = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.color_name} : {self.product.product_name}"


class ProductImage(models.Model):
    product_image = models.ImageField(upload_to='product_images_colors/')
    product_color = models.ForeignKey(ProductColor, related_name='product_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"ProductImage - {self.product_color.color_name}"


class Category(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    category_icon = models.CharField(max_length=333, null=True, blank=True)
    category_image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    category_slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ManyToManyField('self', symmetrical=False, related_name='subcategories', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Review(models.Model):
    reviewer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField(validators=[ MinValueValidator(1), MaxValueValidator(5),])
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f"Reviewer {self.reviewer} : Product {self.product}"
    
    class Meta:
        ordering = ('-updated', 'created')
        unique_together = ('reviewer', 'product')


class PasswordResetCode(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(minutes=3)

        return self.created < expiration_time


class WishList(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer_wishlist = models.ForeignKey(Customer, on_delete=models.CASCADE)
    add_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Wish List"


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_amount = models.DecimalField(decimal_places=2, max_digits=5)
    expiration_date  = models.DateField()
    minimum_amount = models.DecimalField(decimal_places=2, max_digits=14)

    def is_expired(self):
        now = timezone.now().date()
        if self.expiration_date >= now: return False
        return True
    
    def apply_discount(self, amount):
        if amount >= self.minimum_amount:
            discount = amount * (self.discount_amount / 100)
            return round(amount - discount, 2)
        return amount
    
    def __str__(self): return f"{self.code}"            


class Subscription(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    subscribed_email = models.CharField(max_length=200)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return 'Subscription'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)
    completed = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True)



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=122)
    house_number = models.CharField(max_length=122)
    address = models.CharField(max_length=122)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)



