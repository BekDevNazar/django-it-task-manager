from datetime import timedelta

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, TaskType


class TaskPermissionTests(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="Test321test",
        )
        self.manager = get_user_model().objects.create_user(
            username="manager",
            password="TestManager1",
        )
        self.task_type = TaskType.objects.create(
            name="Bug"
        )

        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now() + timedelta(days=1),
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
        )
        manager_group = Group.objects.create(name="Manager")
        add_task_permission = Permission.objects.get(codename="add_task",
                                                     content_type__app_label="tasks")
        add_update_permission = Permission.objects.get(codename="change_task",
                                                       content_type__app_label="tasks")
        add_delete_permission = Permission.objects.get(codename="delete_task",
                                                       content_type__app_label="tasks")
        manager_group.permissions.add(add_task_permission)
        self.manager.groups.add(manager_group)
        manager_group.permissions.add(add_update_permission)
        manager_group.permissions.add(add_delete_permission)

    def test_worker_cannot_open_task_create_page(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("tasks:task-create"),
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_open_task_create_page(self):
        self.client.force_login(self.manager)
        response = self.client.get(
            reverse("tasks:task-create"),
        )
        self.assertEqual(response.status_code, 200)

    def test_worker_cannot_open_change_task_page(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("tasks:task-update", kwargs={"pk": self.task.id}),
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_open_change_task_page(self):
        self.client.force_login(self.manager)
        response = self.client.get(
            reverse("tasks:task-update", kwargs={"pk": self.task.id}),
        )
        self.assertEqual(response.status_code, 200)

    def test_worker_cannot_delete_task(self):
        self.client.force_login(self.worker)

        response = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": self.task.id}),
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_manager_can_delete_task(self):
        self.client.force_login(self.manager)

        response = self.client.post(
            reverse("tasks:task-delete", kwargs={"pk": self.task.id}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_assigned_worker_can_toggle_task_status(self):
        self.task.assignees.add(self.worker)

        self.client.force_login(self.worker)

        response = self.client.post(
            reverse(
                "tasks:task-toggle-status",
                kwargs={"pk": self.task.id},
            )
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_completed)

    def test_unassigned_worker_cannot_toggle_task_status(self):
        self.client.force_login(self.worker)

        response = self.client.post(
            reverse(
                "tasks:task-toggle-status",
                kwargs={"pk": self.task.id},
            )
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.task.is_completed)

    def test_manager_can_toggle_task_status(self):
        self.client.force_login(self.manager)

        response = self.client.post(
            reverse(
                "tasks:task-toggle-status",
                kwargs={"pk": self.task.id},
            )
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_completed)
