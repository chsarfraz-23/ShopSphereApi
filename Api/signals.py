from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def get_or_create_user_cart(sender, instance, created, **kwargs):
    """
    Automatically create a Cart for each newly registered user or retrieves if already registered.
    Uses on_commit to ensure the user is fully saved before cart creation.
    """
    if not created:
        return
    # Use transaction.on_commit so the cart is created *after* the user is committed
    def create_cart():
        Cart.objects.get_or_create(user=instance)
    transaction.on_commit(create_cart)