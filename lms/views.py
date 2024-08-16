from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Выводит все курсы"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
        return [permission() for permission in self.permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Получение списка и создание уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_permissions(self):
        if self.request.method == 'POST':  # Для создания уроков
            self.permission_classes = [IsAuthenticated]  # Только авторизованные пользователи
        else:  # Для получения списка уроков
            self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]  # Авторизованные пользователи + модераторы
        return [permission() for permission in self.permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:  # Обновление уроков
            self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
        elif self.request.method == 'DELETE':  # Удаление уроков
            self.permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
        else:
            self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
        return [permission() for permission in self.permission_classes]




# class CourseLessonCountViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Course.objects.all()
#         serializer = CourseLessonCountSerializer(queryset, many=True)
#         return Response(serializer.data)


