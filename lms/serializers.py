from rest_framework.serializers import ModelSerializer
from lms.models import Course, Lesson
from rest_framework import serializers


# class CourseSerializer(ModelSerializer):
#     class Meta:
#         model = Course
#         fields = "__all__"

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        #fields = ['id', 'title', 'lessons_count']
        fields = ['id', 'title', 'description', 'preview', 'lessons', 'lessons_count', 'owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()



# class CourseLessonCountSerializer(serializers.ModelSerializer):
#     lessons_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Course
#         fields = ['id', 'title', 'lessons_count']
#
#     def get_lessons_count(self, obj):
#         return obj.lessons.count()
