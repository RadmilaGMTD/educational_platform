from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Add test payments to the database"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            email="rmiftyaeva@mail.ru",
            defaults={"password": "radmila68", "first_name": "Radmila", "last_name": "Miftyaeva"},
        )

        course, _ = Course.objects.get_or_create(
            id=3,
            defaults={
                "name": "Естественные науки",
            },
        )
        lesson, _ = Lesson.objects.get_or_create(id=3, defaults={"name": "Химия", "course": course})

        payments = [
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": None,
                "amount": Decimal("4000.00"),
                "payment_method": "cash",
            },
            {
                "user": user,
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": Decimal("1000.00"),
                "payment_method": "transfer",
            },
        ]
        for payment_date in payments:
            payment, created = Payment.objects.get_or_create(**payment_date, defaults={"payment_date": timezone.now()})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added payment: {payment.user} {payment.amount}"))
            else:
                self.stdout.write(self.style.WARNING(f"Payment already exists: {payment.user} {payment.amount}"))
