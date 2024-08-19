from rest_framework.serializers import ModelSerializer
from lms.models import Course, Lesson
from rest_framework import serializers


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

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
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        #fields = ['id', 'title', 'lessons_count']
        fields = ['id', 'title', 'description', 'preview', 'lessons', 'lessons_count', 'owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

