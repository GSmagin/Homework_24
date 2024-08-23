from rest_framework.routers import SimpleRouter
from django.urls import path, include
from lms.views import (CourseViewSet, LessonListView, LessonCreateView, LessonDetailView, LessonUpdateView,
                       LessonDeleteView, SubscriptionCreateDeleteAPIView)
from lms.apps import LmsConfig
from rest_framework import routers

app_name = LmsConfig.name

#router = SimpleRouter()
router = routers.DefaultRouter()

router.register('course', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('payment/', SubscriptionCreateDeleteAPIView.as_view(), name='payment-list-create'),
    # path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    # path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    # path('course/', CourseViewSet.as_view(), name='course-list'),
    # path('courses/lessons-count/', CourseLessonCountViewSet.as_view({'get': 'list'}), name='courses-lessons-count'),
]

urlpatterns += router.urls
