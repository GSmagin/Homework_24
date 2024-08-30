from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from lms.models import Course, Lesson, Subscription
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner, IsModerator
from .pagination import LMSPagination
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from lms.tasks import send_update_course_email


class CourseViewSet(viewsets.ModelViewSet):
    """Выводит все курсы"""
    queryset = Course.objects.all().order_by('id')  # Сортировка по полю 'id'
    serializer_class = CourseSerializer
    pagination_class = LMSPagination
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        course = self.get_object()
        last_course_update = course.time_update

        course.time_update = timezone.now()
        course.save()

        serializer.save()

        if last_course_update < timezone.now() - timedelta(hours=4):
            print(course.time_update)
            send_update_course_email.delay(course.id)

    def get_queryset(self):
        """Переопределение queryset для фильтрации курсов по пользователю"""
        user = self.request.user
        queryset = Course.objects.all()  # По умолчанию берем все курсы

        if user.groups.filter(name='Moderators').exists():
            # Если пользователь модератор, возвращаем все курсы
            queryset = queryset.order_by('id')  # Добавляем сортировку
        else:
            # Если пользователь не модератор, возвращаем только курсы, которые он создал
            queryset = queryset.filter(owner=user).order_by('id')  # Добавляем сортировку

        return queryset

    def perform_create(self, serializer):
        """Назначение владельца при создании курса"""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Назначение прав доступа на основе действия"""
        if self.request.method == ['GET']:
            self.permission_classes = [IsAuthenticated | IsOwner]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        return [permission() for permission in self.permission_classes]


class LessonListView(generics.ListAPIView):
    """Получение списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LMSPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, IsOwner]  # Проверка на владельца и аутентификацию
        return [permission() for permission in self.permission_classes]
    # Проверка на аутентификацию


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonDetailView(generics.RetrieveAPIView):
    """Получение одного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonUpdateView(generics.UpdateAPIView):
    """Получение, обновление и удаление одного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]


class SubscriptionDetailAPIView(views.APIView, LMSPagination):

    def get(self, *args, **kwargs):
        subs = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(subs, self.request)
        serializer = SubscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscriptionCreateDeleteAPIView(APIView, LMSPagination):

    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        response = {
            'subscription_all': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})



