from rest_framework.routers import SimpleRouter
from django.urls import path, include
from lms.views import (LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView,
                       CourseViewSet)
from lms.apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    path('courses/', CourseViewSet.as_view({'get': 'list'}), name='course-list'),
#    path('courses/lessons-count/', CourseLessonCountViewSet.as_view({'get': 'list'}), name='courses-lessons-count'),
]
urlpatterns += router.urls
