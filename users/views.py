from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment, User
from .permissions import IsOwner
from .serializers import PaymentSerializer, PublicUserSerializer, UserSerializer
from .services import create_price, create_product, create_session


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            return UserSerializer
        if self.action == "retrieve":
            if self.get_object() == self.request.user:
                return UserSerializer
            return PublicUserSerializer
        elif self.action == "list":
            return PublicUserSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.is_active = True
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "destroy"]:
            self.permission_classes = (IsOwner,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class PaymentListApiView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_product(payment)
        price = create_price(payment.amount, product)
        session_id, payment_link = create_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
