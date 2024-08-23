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


# class SubscriptionTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email="test@mail.com", password="test")
#         self.course = Course.objects.create(title="Test course", description="Test course description")
#         self.subscription = Subscription.objects.create(user=self.user, course=self.course)
#
#         self.client.force_authenticate(user=self.user)
#
#     def test_subscription_on_off(self):
#         url = reverse("lms:payment-list-create")
#         data = {
#             "course_id": self.course.id,
#             "user": self.user.id
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(
#             response.status_code, status.HTTP_200_OK
#         )
#         print(response.data.get("message"))
#         self.assertIn("Подписка добавлена", response.data.get("message"))
#
#         response = self.client.delete(url, data={"course_id": self.course.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("Подписка удалена", response.data.get("message"))
