from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task()
def send_update_materials(course_name, email):
    send_mail("Обновление курса", f"Курс '{course_name}' обновился!", EMAIL_HOST_USER, [email])
