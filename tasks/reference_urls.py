from django.urls import path

from tasks.reference_views import (TaskTypeListView,
                                   TaskTypeUpdateView,
                                   TaskTypeCreateView,
                                   TaskTypeDeleteView,
                                    PositionListView,
                                   PositionCreateView,
                                   PositionDeleteView,
                                   PositionUpdateView)

app_name = "references"
urlpatterns = [
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
]
