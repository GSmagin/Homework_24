from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied

from lms.models import Course, Lesson
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrOwner, IsOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Выводит все курсы"""
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Фильтрует список курсов, чтобы показывать только те, которые принадлежат текущему пользователю
        или все курсы, если пользователь является модератором.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists():
                return Course.objects.all()
            return Course.objects.filter(owner=user)
        return Course.objects.none()  # Если пользователь не аутентифицирован, возвращаем пустой queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsModeratorOrOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Получение списка и создание уроков"""
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Фильтрует список уроков, чтобы показывать все уроки модераторам
        и только уроки, принадлежащие текущему пользователю, для обычных пользователей.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists():
                # Если пользователь является модератором, возвращаем все уроки
                return Lesson.objects.all()
            else:
                # Если пользователь не модератор, возвращаем только его уроки
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()  # Если пользователь не аутентифицирован, возвращаем пустой queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsOwner]  # Проверка на владельца и аутентификацию
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            # Если пользователь модератор, запрещаем создание урока
            raise PermissionDenied("Модераторам запрещено создавать уроки.")
        # Сохраняем урок с привязкой к текущему пользователю
        serializer.save(owner=user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsModeratorOrOwner]  # Модераторы и владельцы могут обновлять
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]  # Только владельцы могут удалять
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



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


