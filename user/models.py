from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
import uuid
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class UserManager(AbstractUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given  email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
     
    def create_user(self,email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email=email, password=password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

USER_TYPE = [
        ("admin", "Admin"),
        ("user", "Users"),    ]

class User(AbstractUser):
    # user_name = None
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13,unique=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=15, default='user')
    joining_date = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=False, blank=True, null=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return "{}".format(self.email)



        
    