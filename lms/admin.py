from django.contrib import admin
from users.models import Payment
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'preview', 'description', 'owner']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'preview', 'description']
    list_filter = ['title', 'preview', 'description']
    list_editable = ['preview', 'owner']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course', 'preview', 'video_url', 'owner']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'title']
    list_filter = ['id']
    list_editable = ['course', 'owner']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'course', 'lesson', 'amount', 'payment_method']
    list_filter = ['payment_method', 'date']
    search_fields = ['user__username', 'course__title', 'lesson__title']
