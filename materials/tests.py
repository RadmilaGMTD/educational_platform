from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson, Subscription


class MaterialsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test_user@mail.ru")
        self.course = Course.objects.create(name="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(name="Тестовый урок", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_course(self):
        response = self.client.get(f"/courses/{self.course.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_create_course(self):
        data = {"name": "Тестовый курс 2"}
        response = self.client.post("/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_update_course(self):
        data = {"name": "Тестовый курс 3"}
        response = self.client.patch(f"/courses/{self.course.pk}/", data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тестовый курс 3")

    def test_delete_course(self):
        response = self.client.delete(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_list_course(self):
        response = self.client.get("/courses/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 8,
                        "count_lessons": 1,
                        "lessons": [
                            {
                                "id": 8,
                                "name": "Тестовый урок",
                                "image": None,
                                "description": None,
                                "video_url": None,
                                "course": 8,
                                "owner": 7,
                            }
                        ],
                        "is_subscribed": False,
                        "name": "Тестовый курс",
                        "image": None,
                        "description": None,
                        "owner": 7,
                    }
                ],
            },
        )

    def test_retrieve_lesson(self):
        response = self.client.get(f"/courses/lessons/{self.lesson.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_create_lesson(self):
        data = {"name": "Тестовый урок 2"}
        response = self.client.post("/courses/lessons/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_update_lesson(self):
        data = {"name": "Тестовый урок 3"}
        response = self.client.patch(f"/courses/lessons/update/{self.lesson.pk}/", data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тестовый урок 3")

    def test_delete_lesson(self):
        response = self.client.delete(f"/courses/lessons/delete/{self.lesson.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_lessons(self):
        response = self.client.get("/courses/lessons/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 9,
                        "name": "Тестовый урок",
                        "image": None,
                        "description": None,
                        "video_url": None,
                        "course": 9,
                        "owner": 8,
                    }
                ],
            },
        )

    def test_create_subscription(self):
        self.assertEqual(Subscription.objects.count(), 0)
        response = self.client.post("/courses/subscription/create/", {"id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertEqual(Subscription.objects.count(), 1)

    def test_delete_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(
            "/courses/subscription/create/",
            {"id": self.course.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertEqual(Subscription.objects.count(), 0)
