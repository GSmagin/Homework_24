from django.core.mail import send_mail
from celery import shared_task

from confing.settings import EMAIL_HOST_USER
from lms.models import Subscription, Course


# @shared_task
# def send_update_course_email(course_id):
#     subscriptions = Subscription.objects.select_related("course").filter(course_id=course_id)
#     if subscriptions:
#         course = subscriptions.first().course
#         send_mail(
#             "Обновление курса",
#             f"Курс '{course.title}' был успешно обновлен",
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[subscription.user.email for subscription in subscriptions]
#         )

@shared_task
def send_update_course_email(course_id: int) -> None:
    course = Course.objects.filter(pk=course_id).first()
    if not course:
        return

    course_subscriptions = Subscription.objects.filter(course=course)
    emails = course_subscriptions.values_list('user__email', flat=True)
    if emails:
        send_mail(
            "Обновление курса",
            f"Курс '{course.title}' был успешно обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=emails
        )
