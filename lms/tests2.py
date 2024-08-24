from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.group = Group.objects.create(name="Moderators")
        self.moder = User.objects.create(email="moder@mail.com", password="modertest")
        self.moder.groups.add(self.group)
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.user2 = User.objects.create(email="test2@mail.com", password="test2")

        self.course = Course.objects.create(title="Test course", description="Test course description")
        self.lesson = Lesson.objects.create(title="Test lesson", description="Test lesson description",
                                            video_url="https://www.youtube.com/watch?v=gomh",
                                            course=self.course,
                                            owner=self.user)
        self.lesson2 = Lesson.objects.create(title="Test lesson 2", description="Test lesson description 2",
                                             video_url="https://www.youtube.com/watch?v=gomhM",
                                             course=self.course,
                                             owner=self.user2)

        self.client.force_authenticate(user=self.user)

    def test_lesson_list_unauthenticated(self):
        # Проверяем, что неавторизованный пользователь не может получить список уроков
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = reverse("lms-api:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_detail_unauthenticated(self):
        # Проверяем, что неавторизованный пользователь не может получить детали урока
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = reverse("lms:lesson-detail", args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_moderator_access(self):
        # Проверяем, что модератор может получить доступ к уроку, даже если он ему не принадлежит
        self.client.force_authenticate(user=self.moder)  # Авторизация как модератор
        url = reverse("lms:lesson-detail", args=[self.lesson2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.lesson2.title)

    def test_moderator_can_update_any_lesson(self):
        # Проверяем, что модератор может редактировать любой урок
        self.client.force_authenticate(user=self.moder)  # Авторизация как модератор
        url = reverse("lms:lesson-update", args=[self.lesson2.id])
        data = {
            "title": "Moderator updated lesson",
            "description": "Moderator updated lesson description",
            "video_url": "https://www.youtube.com/watch?v=newlink",
            "course": self.course.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "Moderator updated lesson")

    def test_moderator_cannot_delete_lesson(self):
        # Проверяем, что модератор не может удалить урок
        self.client.force_authenticate(user=self.moder)  # Авторизация как модератор
        url = reverse("lms:lesson-delete", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_cannot_create_lesson(self):
        # Проверяем, что неавторизованный пользователь не может создать урок
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = reverse("lms:lesson-create")
        data = {
            "title": "New Unauthorized Lesson",
            "description": "New lesson description",
            "video_url": "https://www.youtube.com/watch?v=unauthorized",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_cannot_update_lesson(self):
        # Проверяем, что неавторизованный пользователь не может обновить урок
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = reverse("lms:lesson-update", args=[self.lesson.id])
        data = {
            "title": "Updated lesson by unauthorized",
            "description": "Updated description",
            "video_url": "https://www.youtube.com/watch?v=update",
            "course": self.course.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_cannot_delete_lesson(self):
        # Проверяем, что неавторизованный пользователь не может удалить урок
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = reverse("lms:lesson-delete", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        url = reverse("lms-api:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.id,
                    "title": self.lesson.title,
                    "preview": self.lesson.preview,
                    "description": self.lesson.description,
                    "video_url": self.lesson.video_url,
                    "course": self.course.id,
                    "owner": self.user.id
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_lesson_detail(self):
        # Тестовый доступ к уроку, принадлежащему авторизованному пользователю
        url = reverse("lms:lesson-detail", args=[self.lesson.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

        # Тестовый доступ к уроку, не принадлежащему авторизованному пользователю
        url = reverse("lms:lesson-detail", args=[self.lesson2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # ???

    def test_create_lesson(self):
        url = reverse("lms:lesson-create")
        data = {
            "title": "New test lesson",
            "description": "New test lesson description",
            "video_url": "https://www.youtube.com/watch?v=gomhMmutBd9",
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 3
        )

    def test_update_lesson(self):
        url = reverse("lms:lesson-update", args=(self.lesson.id,))
        data = {
            "title": "Updated test lesson",
            "description": "Updated test lesson description",
            "video_url": "https://www.youtube.com/watch?v=gomhMmutBd10",
            "course": self.course.id
        }
        response = self.client.put(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "Updated test lesson"
        )

        url = reverse("lms:lesson-update", args=(self.lesson2.id,))
        response = self.client.put(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_delete_lesson(self):
        url = reverse("lms:lesson-delete", args=(self.lesson.id,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

        url = reverse("lms:lesson-delete", args=(self.lesson2.id,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_moder_can_update_lesson(self):
        self.client.force_authenticate(user=self.moder)

        url = reverse("lms:lesson-update", args=(self.lesson.id,))
        data = {
            "title": "Moder updated test lesson",
            "description": "Moder updated test lesson description",
            "video_link": "https://www.youtube.com/watch?v=gomhMmutBd11",
            "course": self.course.id
        }
        response = self.client.put(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "Moder updated test lesson"
        )

    def test_moder_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moder)

        url = reverse("lms:lesson-delete", args=(self.lesson.id,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.course = Course.objects.create(title="Test course", description="Test course description")

        self.client.force_authenticate(user=self.user)

    def test_subscription_on_off(self):
        url = reverse("lms:payment-list-create")
        data = {
            "course_id": self.course.id,
            "user": self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIn("Подписка добавлена", response.data.get("message"))
        response = self.client.post(url, data={"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка удалена", response.data.get("message"))


class SubscriptionTestCaseNoAuth(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password="test")
        self.course = Course.objects.create(title="Test course", description="Test course description")

    def test_subscription_on_off(self):
        url = reverse("lms:payment-list-create")
        data = {
            "course_id": self.course.id,
            "user": self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        response = self.client.post(url, data={"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
