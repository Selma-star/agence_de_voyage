from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from Core.models import Client  # Import your custom user model

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            client = Client.objects.get(email=email)  # Search by email
            if client and check_password(password, client.password):  # Verify password
                return client
        except Client.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None
