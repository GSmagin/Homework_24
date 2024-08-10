from django.urls import path
from .views import UserProfileAPIView, PaymentListAPIView, UserDetailAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('profile/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
]
