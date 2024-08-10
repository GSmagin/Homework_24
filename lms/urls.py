from rest_framework.routers import SimpleRouter
from django.urls import path, include
from lms.views import (LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView, CourseLessonCountViewSet,
                       CourseViewSet)
from lms.apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    path('courses/lessons-count/', CourseLessonCountViewSet.as_view({'get': 'list'}), name='courses-lessons-count'),
]
urlpatterns += router.urls
