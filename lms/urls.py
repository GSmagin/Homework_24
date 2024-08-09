from rest_framework.routers import SimpleRouter
from django.urls import path, include
from lms.views import LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView, CourseViewSet
from lms.apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
#    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]
urlpatterns += router.urls
