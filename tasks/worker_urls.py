from django.urls import path

from tasks.worker_views import WorkerListView, WorkerDetailView

app_name = "workers"
urlpatterns = [
  path("", WorkerListView.as_view(), name="worker-list"),
  path("<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]