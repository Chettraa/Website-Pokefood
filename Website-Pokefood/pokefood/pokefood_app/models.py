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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()