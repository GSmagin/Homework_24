from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from lms.models import Course, Lesson, Subscription
from rest_framework import serializers

from lms.validators import CheckLinkVideo


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [CheckLinkVideo(field='video_url')]

    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)
        lesson.owner = self.context['request'].user
        return lesson

    def update(self, instance, validated_data):
        for field in self.get_fields():
            if field == 'owner':  # При правке модератором не меняем владельца
                continue
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    lessons_count = serializers.IntegerField(source='lesson.count', read_only=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'time_update', 'description', 'preview', 'owner', 'lessons', 'lessons_count', 'is_subscribed']

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        course.owner = self.context['request'].user
        return course

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_subscription(self, obj):
        user = self.context['request'].user
        return obj.subscription.filter(user=user).exists()

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'course',
            ]

