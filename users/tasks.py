from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_users():
    block_users = User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30), is_active=True)
    block_users.update(is_active=False)
