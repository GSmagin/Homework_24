from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    """Выводит все курсы"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Получение списка и создание уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# class CourseLessonCountViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Course.objects.all()
#         serializer = CourseLessonCountSerializer(queryset, many=True)
#         return Response(serializer.data)


