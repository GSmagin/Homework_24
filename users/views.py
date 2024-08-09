from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем текущего авторизованного пользователя
        return self.request.user
