from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import User


@shared_task()
def user_blocking():
    now = timezone.now()
    inactive_users = User.objects.filter(last_login__lt=now - timedelta(days=30), is_active=True, is_superuser=False)
    if inactive_users.exists():
        inactive_users.update(is_active=False)
