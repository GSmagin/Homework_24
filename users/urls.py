from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserListCreateAPIView, UserDetailAPIView, UserRegistrationAPIView, UserProfileRetrieveUpdateAPIView, \
    PaymentListAPIView, UserProfileAPIView

urlpatterns = [
     path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    # path('profile/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('list/', UserListCreateAPIView.as_view(), name='user-list'),
    path('detail/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
]
