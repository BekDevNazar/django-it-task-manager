from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views import generic

from tasks.models import Worker


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "workers"
    paginate_by = 5

    def get_queryset(self):
        return (
            Worker.objects
            .select_related("position")
            .annotate(task_count=Count("tasks"))
            .order_by("username")
        )


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = 'workers/worker_detail.html'
    context_object_name = "worker"

    def get_queryset(self):
        return Worker.objects.select_related("position").prefetch_related("tasks")


