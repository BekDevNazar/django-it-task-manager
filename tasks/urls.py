from django.urls import path

from tasks.views import TaskListView, TaskDetailView, TaskUpdateView, TaskCreateView, TaskDeleteView, toggle_task_status

app_name = "tasks"
urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/toggle-status/", toggle_task_status, name="task-toggle-status",)
]