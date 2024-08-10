from rest_framework.serializers import ModelSerializer
from lms.models import Course, Lesson
from rest_framework import serializers


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseLessonCountSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
