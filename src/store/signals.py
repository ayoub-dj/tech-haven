from .utils import create_unique_slug
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Product, Category


@receiver(pre_save, sender=Product)
def set_product_slug(sender, instance, *args, **kwargs):
    if not instance.product_slug:
        instance.product_slug = create_unique_slug(instance.product_name, 'product')

@receiver(pre_save, sender=Category)
def set_category_slug(sender, instance, *args, **kwargs):
    if not instance.category_slug:
        instance.category_slug = create_unique_slug(instance.name, 'category')