from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson, Subscription
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

User = get_user_model()


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, "Test Course")
        self.assertEqual(self.course.owner, self.user)

    def test_course_str(self):
        self.assertEqual(str(self.course), self.course.title)


class LessonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            owner=self.user,
        )

    def test_lesson_creation(self):
        self.assertEqual(self.lesson.title, "Test Lesson")
        self.assertEqual(self.lesson.course, self.course)

    def test_lesson_str(self):
        self.assertEqual(str(self.lesson), self.lesson.title)


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user
        )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.course, self.course)

    def test_subscription_str(self):
        expected_str = f'{self.user} подписался на {self.course}'
        self.assertEqual(str(self.subscription), expected_str)


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)

    def test_subscription_creation(self):
        url = reverse('lms:payment-list-create')  # Убедитесь, что у вас есть этот маршрут в urls.py
        data = {
            'course_id': self.course.id
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.latest('id').user, self.user)

    def test_subscription_list(self):
        url = reverse('lms-api:payment-list-create')  # Убедитесь, что у вас есть этот маршрут в urls.py
        response = self.client.get(url)
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('subscription_all', response.data)
        self.assertEqual(len(response.data['subscription_all']), 1)  # Учитываем одну подписку

    def test_subscription_deletion(self):
        url = reverse('lms-api:payment-list-create')  # Убедитесь, что у вас есть этот маршрут в urls.py
        data = {
            'course_id': self.course.id
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)  # Подписка удалена


class CourseViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_get_course_list(self):
        response = self.client.get(reverse('lms:course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_course(self):
        data = {
            'title': 'New Course',
            'description': 'New Course Description'
        }
        response = self.client.post(reverse('lms:course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        data = {
            'title': 'Updated Course',
            'description': 'Updated Description'
        }
        response = self.client.put(reverse('lms:course-detail', kwargs={'pk': self.course.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course')

    def test_delete_course(self):
        response = self.client.delete(reverse('lms:course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)