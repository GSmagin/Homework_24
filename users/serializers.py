from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'date_joined', 'last_login', 'payments']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_payments(self, obj):
        # Фильтруем платежи для данного пользователя
        payments = Payment.objects.filter(user=obj)
        return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    lesson_title = serializers.SerializerMethodField()
    payment_method_display = serializers.CharField(source='get_payment_method_display')

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'date', 'course', 'course_title', 'lesson', 'lesson_title', 'amount', 'payment_method', 'payment_method_display']

    def get_user_email(self, obj):
        return obj.user.email

    def get_course_title(self, obj):
        if obj.course:
            return obj.course.title
        return None

    def get_lesson_title(self, obj):
        if obj.lesson:
            return obj.lesson.title
        return None
