from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
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

    def to_representation(self, instance):
        """
        Возвращает разные поля в зависимости от того, кто запрашивает данные.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request', None)

        if request and request.user != instance:
            # Если запрашивает не владелец, скрываем чувствительные данные
            representation.pop('last_name', None)
            representation.pop('password', None)
            # Например, если у вас есть поле с историей платежей:
            representation.pop('payment_history', None)
        return representation


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            city=validated_data['city'],
            avatar=validated_data.get('avatar')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class UserSerializer(serializers.ModelSerializer):
#     payments = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'phone', 'city', 'avatar', 'date_joined', 'last_login', 'payments']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }
#
#     def get_payments(self, obj):
#         # Фильтруем платежи для данного пользователя
#         payments = Payment.objects.filter(user=obj)
#         return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    lesson_title = serializers.SerializerMethodField()
    payment_method_display = serializers.CharField(source='get_payment_method_display')

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'date', 'course', 'course_title', 'lesson', 'lesson_title', 'amount',
                  'payment_method', 'payment_method_display']

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
