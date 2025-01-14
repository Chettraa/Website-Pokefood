from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class LoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"
    
class RegisterRecord(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            register_time = models.DateTimeField(default=now)
            email = models.EmailField(unique=True)
            ip_address = models.GenericIPAddressField(null=True, blank=True)

            def __str__(self):
                return f"{self.user.username} registered at {self.register_time}"
            
            
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ... other product fields

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    # ... other order fields (e.g., order status)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Prevent product deletion if it has orders
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.pk}"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()