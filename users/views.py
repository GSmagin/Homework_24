from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .permissions import IsOwner
from .serializers import UserRegistrationSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import UserSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product

User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class SomeProtectedView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи

    def get_queryset(self):
        """
        Ограничиваем доступ к профилям, чтобы они были видны только авторизованным пользователям.
        """
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        """
        Получаем объект пользователя для показа или редактирования.
        """
        return User.objects.get(pk=self.kwargs['pk'])


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем текущего авторизованного пользователя
        # return self.request.user

        return User.objects.get(user=self.request.user)


class PaymentListAPIView(generics.ListAPIView):
    # queryset = Payment.objects.all()
    # serializer_class = PaymentSerializer
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset_class = PaymentFilter

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        # Ограничиваем queryset только платежами текущего пользователя
        return super().get_queryset().filter(user=self.request.user)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.course)
        price = create_stripe_price(payment.amount, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


