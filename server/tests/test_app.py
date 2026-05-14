from django.test import TestCase
from django.test import Client
from application.models import Task
from application.models import Profile
from datetime import datetime

# Tasks are handled properly on the server side
class TasksCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/signup/submit/',
            data = {
                "first_name": "John",
                "last_name": "Appleseed",
                "dob": "2001-01-01",
                "email": "johnappleseed@outlook.com",
                "display_name": "JATask",
                "password": "1lov3tasks"
            },
            content_type='application/json'
        )

        self.profile = Profile.objects.get(user__email="johnappleseed@outlook.com")

        self.client.post(
            '/login/submit/',
            data = {
                "email": "johnappleseed@outlook.com",
                "password": "1lov3tasks"
            },
            content_type='application/json'
        )

    """
    A task with deadline after now, reminder between now and the deadline and a title
    should be created successfully
    """
    def test_create_task_1(self):
        response = self.client.post(
            '/add_task/',
            data = {
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "rWUu1CgfBy2nbUwDRk1Ui5WnnFRj86Aez6WD"
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    """
    A task with no title should not be created
    """
    def test_create_task_2(self):
        response = self.client.post(
            '/add_task/',
            data={
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "zmyW8ndgw2xt2jFgUZ2nJ7JF3kfvjc7iZXUb"
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    """
    A task with no deadline or a deadline before now should not be created
    """
    def test_create_task_3(self):
        response = self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "remind_at": "2026-11-13T08:00",
                "task_id": "DCKG8WkNkHK0WmkEz36L3NZ52bkn6P9nPtLy"
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    """
    A task with the reminder after the deadline or before now should not be created
    """
    def test_create_task_4(self):
        response = self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2028-11-13T08:00",
                "task_id": "nZ4MafanHQytnxfQwfBkTjCDFiRYiPHAWxKK"
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    """
    When the task is removed using this method, do not add XP or levels to the
    user's profile.
    """
    def remove_task(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "Complete homework",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "UkerXzCv9wtK0wUrNzWqgSvXbSFGSJXVqarA"
            },
            content_type='application/json'
        )

        response = self.client.post(
            '/remove_task/',
            data = {
                "task_id": "UkerXzCv9wtK0wUrNzWqgSvXbSFGSJXVqarA"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.xp, 0)
        self.assertEqual(self.profile.level, 1)

    """
    Add note, change title and modify deadline and reminder of the task
    """
    def test_edit_task_1(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "07WqUw8uXt5pYWRpLvux8rUnJp5p065aN40H"
            },
            content_type='application/json'
        )

        response = self.client.post(
            '/edit_task/',
            data={
                "title": "My best task",
                "notes": "I can't wait to complete this task!",
                "task_id": "07WqUw8uXt5pYWRpLvux8rUnJp5p065aN40H"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    """
    Add reminder to task
    """
    def test_edit_task_2(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "ywcLnecXFieTaT0XScdK4m27TyZ2UZ7RGGtH"
            },
            content_type='application/json'
        )

        response = self.client.post(
            '/edit_task/',
            data={
                "remind_at": "2026-12-13T08:00",
                "task_id": "ywcLnecXFieTaT0XScdK4m27TyZ2UZ7RGGtH"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    """
    Don't modify task if the new parameters are invalid
    """
    def test_edit_task_3(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "reVi9eG1zqZLv9N19a7cCxHeBdZUMqbNniAf"
            },
            content_type='application/json'
        )

        response = self.client.post(
            '/edit_task/',
            data={
                "title": "",
                "deadline": "2025-05-13T08:00",
                "task_id": "reVi9eG1zqZLv9N19a7cCxHeBdZUMqbNniAf"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


# Ensure the user correctly levels up and receives XP upon completion of a task
class LevelsAndXPTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(
            '/signup/submit/',
            data = {
                "first_name": "John",
                "last_name": "Appleseed",
                "dob": "2001-01-01",
                "email": "johnappleseed@outlook.com",
                "display_name": "JATask",
                "password": "1lov3tasks"
            },
            content_type='application/json'
        )
        self.client.post(
            '/login/submit/',
            data = {
                "email": "johnappleseed@outlook.com",
                "password": "1lov3tasks"
            },
            content_type='application/json'
        )

        self.profile = Profile.objects.get(user__email="johnappleseed@outlook.com")

    """
    The task is completed, add XP to the user
    """
    def task_complete_no_level_up(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "RLw6ikmXvM6rPStJ7RiiEBvk9Bu38deGfQx4"
            },
            content_type='application/json'
        )

        response = self.client.post(
            '/complete_task/',
            data = {
                "task_id": "RLw6ikmXvM6rPStJ7RiiEBvk9Bu38deGfQx4"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.xp, 20)
        self.assertEqual(self.profile.level, 1)

    """
    The task is completed, and the user has enough XP to level up, increase the level and clamp
    XP to 0. 
    """
    def task_complete_with_level_up(self):
        self.client.post(
            '/add_task/',
            data={
                "title": "New Task",
                "deadline": "2027-05-13T08:00",
                "remind_at": "2026-11-13T08:00",
                "task_id": "mS7mkx2BPF7FHV5bHiyq6ur644hp0p8egjvt"
            },
            content_type='application/json'
        )

        # Increase XP to 80 to force level up
        self.profile.xp = 80
        self.profile.save()

        response = self.client.post(
            '/complete_task/',
            data = {
                "task_id": "mS7mkx2BPF7FHV5bHiyq6ur644hp0p8egjvt"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.xp, 0)
        self.assertEqual(self.profile.level, 2)
