from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from django.views import generic

from tasks.models import Task, Worker


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        task_stats = Task.objects.aggregate(
            total_tasks=Count("id"),

            completed_tasks=Count(
                "id",
                filter=Q(is_completed=True),
            ),

            active_tasks=Count(
                "id",
                filter=Q(is_completed=False),
            ),

            overdue_tasks=Count(
                "id",
                filter=Q(
                    deadline__lt=now,
                    is_completed=False,
                ),
            ),
        )

        context.update(task_stats)

        context["total_workers"] = Worker.objects.count()

        context["upcoming_tasks"] = (
            Task.objects
            .filter(
                deadline__gte=now,
                is_completed=False,
            )
            .select_related("task_type")
            .order_by("deadline")[:5]
        )

        return context