from datetime import timedelta

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_users():
    month_ago = timezone.now() - relativedelta(months=1)
    block_users = User.objects.filter(last_login__lt=timezone.now() - month_ago, is_active=True)
    block_users.update(is_active=False)
