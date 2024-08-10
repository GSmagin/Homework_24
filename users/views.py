from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import PaymentSerializer

from .filters import PaymentFilter
from .models import Payment
from .serializers import UserSerializer

User = get_user_model()


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем текущего авторизованного пользователя
        return self.request.user


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
