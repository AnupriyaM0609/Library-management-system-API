from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib.auth.backends import BaseBackend, ModelBackend

from .models import User


# class EmailUsernameAuthenticationBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)

#         except User.DoesNotExist:
#             return None

#         if user and check_password(password, user.password):
#             return user
    

class EmailUsernameAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        