from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig

from .views import PaymentListApiView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListApiView.as_view(), name="payments_list"),
] + router.urls
