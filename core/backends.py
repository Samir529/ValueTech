from django.contrib.auth.backends import BaseBackend
from core.models import customUser


class custom_authentication_backend(BaseBackend):
    """
    Authenticate using email or phone number
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Trying to authenticate:", username)
        # Try to find user by email
        user = customUser.objects.filter(email=username).first()
        if user:
            print("Found by email:", user.email)
        else:
            # Try to find user by phone number
            user = customUser.objects.filter(phone_number=username).first()
            if user:
                print("Found by phone number:", user.phone_number)
        if user:
            print("Password valid?", user.check_password(password))
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return customUser.objects.get(pk=user_id)
        except customUser.DoesNotExist:
            return None

