from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

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
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Проверяем, что obj является экземпляром User
            if isinstance(obj, User):
                if obj == request.user:
                    # Фильтруем платежи для данного пользователя
                    payments = Payment.objects.filter(user=request.user)
                    return PaymentSerializer(payments, many=True).data
                else:
                    return []  # Если пользователь не является владельцем, возвращаем пустой список
        return []

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


# class PaymentSerializer(serializers.ModelSerializer):
#     user_email = serializers.SerializerMethodField()
#     course_title = serializers.SerializerMethodField()
#     lesson_title = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Payment
#         fields = [
#             'id',
#             'user',
#             'user_email',
#             'date',
#             'course',
#             'course_title',
#             'lesson',
#             'lesson_title',
#             'amount',
#             'payment_method',
#         ]

    # def get_user_email(self, obj):
    #     # Возвращаем email пользователя
    #     return obj.user.email
    #
    # def get_course_title(self, obj):
    #     # Возвращаем название курса, если оно есть
    #     if obj.course:
    #         return obj.course.title
    #     return None
    #
    # def get_lesson_title(self, obj):
    #     # Возвращаем название урока, если оно есть
    #     if obj.lesson:
    #         return obj.lesson.title
    #     return None

    # def to_representation(self, obj):
    #     request = self.context.get('request')
    #     if request and hasattr(request, 'user'):
    #         if obj.user == request.user:
    #             return super().to_representation(obj)
    #         else:
    #             # Можно вернуть пустой словарь или часть данных
    #             return {}  # Либо return None, если вы хотите, чтобы объект вообще не показывался
    #     return super().to_representation(obj)


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
