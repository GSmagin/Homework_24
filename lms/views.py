from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
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


class CourseViewSet(viewsets.ModelViewSet):
    """Выводит все курсы"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Переопределение queryset для фильтрации курсов по пользователю"""
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            # Если пользователь модератор, возвращаем все курсы
            return Course.objects.all()
        else:
            # Если пользователь не модератор, возвращаем только курсы, которые он создал
            return Course.objects.filter(owner=user)

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


class SubscriptionCreateDeleteAPIView(views.APIView, LMSPagination):

    def post(self, request, *args, **kwargs, ):
        course = self.get_course_or_404(Course, course_id=request.data.get('id'))
        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.title} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=request.data.get('id'))
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.title} удален из подписок',
        }
        # return Response(status=status.HTT_204_NO_CONTENT)
        return Response(response)

    @staticmethod
    def get_course_or_404(course, course_id):
        try:
            return get_object_or_404(course, id=course_id)
        except (TypeError, ValueError, ValidationError, Http404):
            response = {
                'detail': f'Курс с id-{course_id} не найден'
            }
            raise Http404(response)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(exc.args[0], status=404)
        return super().handle_exception(exc)





#
# class LessonListCreateAPIView(generics.ListCreateAPIView):
#     """Получение списка и создание уроков"""
# #    queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.groups.filter(name='Moderators').exists():
#             return Lesson.objects.all()
#         else:
#             return Lesson.objects.filter(owner=user)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             self.permission_classes = [IsAuthenticated, IsOwner]
#         elif self.request.method == 'POST':
#             self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]  # Проверка на владельца и аутентификацию
#         return [permission() for permission in self.permission_classes]
#
#     # def perform_create(self, serializer):
#     #     user = self.request.user
#     #     if user.groups.filter(name='Moderators').exists():
#     #         # Если пользователь модератор, запрещаем создание урока
#     #         raise PermissionDenied("Модераторам запрещено создавать уроки.")
#     #     # Сохраняем урок с привязкой к текущему пользователю
#     #     serializer.save(owner=user)
#
#
# class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Получение, обновление и удаление одного урока"""
# #    queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.groups.filter(name='Moderators').exists():
#             return Lesson.objects.all()
#         else:
#             return Lesson.objects.filter(owner=user)
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             self.permission_classes = [IsAuthenticated]
#         elif self.request.method in ['PUT', 'PATCH']:
#             self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]  # Модераторы и владельцы могут обновлять
#         elif self.request.method == 'DELETE':
#             self.permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]  # Только владельцы могут удалять
#         return [permission() for permission in self.permission_classes]
#
#     def perform_update(self, serializer):
#         serializer.save(owner=self.request.user)
#

# class CourseViewSet(viewsets.ModelViewSet):
#     """Выводит все курсы"""
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#
#     def get_permissions(self):
#         if self.action in ['create', 'destroy']:
#             self.permission_classes = [IsAuthenticated]
#         elif self.action in ['update', 'partial_update']:
#             self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#         else:
#             self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#         return [permission() for permission in self.permission_classes]
#
#
# class LessonListCreateAPIView(generics.ListCreateAPIView):
#     """Получение списка и создание уроков"""
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#
#     def get_permissions(self):
#         if self.request.method == 'POST':  # Для создания уроков
#             self.permission_classes = [IsAuthenticated]  # Только авторизованные пользователи
#         else:  # Для получения списка уроков
#             self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]  # Авторизованные пользователи + модераторы
#         return [permission() for permission in self.permission_classes]
#
#
# class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Получение, обновление и удаление одного урока"""
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#
#     def get_permissions(self):
#         if self.request.method in ['PUT', 'PATCH']:  # Обновление уроков
#             self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#         elif self.request.method == 'DELETE':  # Удаление уроков
#             self.permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
#         else:
#             self.permission_classes = [IsAuthenticated, IsModeratorOrOwner]
#         return [permission() for permission in self.permission_classes]
#
#


# class CourseLessonCountViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Course.objects.all()
#         serializer = CourseLessonCountSerializer(queryset, many=True)
#         return Response(serializer.data)


