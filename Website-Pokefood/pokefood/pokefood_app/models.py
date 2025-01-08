from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

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