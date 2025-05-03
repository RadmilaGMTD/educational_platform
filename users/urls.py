from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from .views import PaymentCreateApiView, PaymentListApiView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListApiView.as_view(), name="payments_list"),
    path("payments/create/", PaymentCreateApiView.as_view(), name="payments_create"),
    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
] + router.urls
