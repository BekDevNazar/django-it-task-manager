from django.urls import path

from tasks.views import TaskListView, TaskDetailView, TaskUpdateView, TaskCreateView

app_name = "tasks"
urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
]