from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username:
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return None
            elif username.isdigit():
                try:
                    user = User.objects.get(phone_number=username)
                except User.DoesNotExist:
                    return None
            else:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return None

            if user and user.check_password(password):
                return user

        return None
