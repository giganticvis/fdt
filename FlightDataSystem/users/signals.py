from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import Log

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    Log.objects.create(user=user, action='login', details=f"User logged in from {request.META.get('REMOTE_ADDR')}")
