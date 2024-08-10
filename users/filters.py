from django_filters import rest_framework as filters
from users.models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name="course__id")
    lesson = filters.NumberFilter(field_name="lesson__id")
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    ordering = filters.OrderingFilter(
        fields=(
            ('date', 'date'),
        ),
        field_labels={
            'date': 'Payment Date',
        }
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']