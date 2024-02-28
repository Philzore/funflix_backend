from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
    
    def create_user(self,username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_guest_user(self):
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        random_string = get_random_string(length=5)
        username = f"guest_{timestamp}_{random_string}"
        useremail = f"guest{timestamp}_{random_string}@guest.de"
        userpassword = f"guest{timestamp}_{random_string}"
        guest_user = self.create_user(username, email=useremail, password=userpassword)
        return guest_user
        