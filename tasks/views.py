from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from tasks.forms import TaskForm, TaskSearchForm
from tasks.models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        return context

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("task_type")
            .prefetch_related("assignees")
        )
        self.search_form = TaskSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            name = self.search_form.cleaned_data["name"]
            description = self.search_form.cleaned_data["description"]
            priorities = self.search_form.cleaned_data["priorities"]
            statuses = set(self.search_form.cleaned_data["statuses"])
            task_types = self.search_form.cleaned_data["task_types"]
            if name:
                queryset = queryset.filter(name__icontains=name)
            if description:
                queryset = queryset.filter(description__icontains=description)
            if priorities:
                queryset = queryset.filter(priority__in=priorities)
            if statuses == {"active"}:
                queryset = queryset.filter(is_completed=False)
            elif statuses == {"completed"}:
                queryset = queryset.filter(is_completed=True)
            if task_types:
                queryset = queryset.filter(task_type__in=task_types)
        return queryset.order_by("is_completed", "deadline")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-list")


@login_required
@require_POST
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    task.is_completed = not task.is_completed
    task.save(update_fields=["is_completed"])

    return redirect("tasks:task-detail", pk=task.pk)


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/my_task_list.html"
    context_object_name = "tasks"
    paginate_by = 5

    def get_queryset(self):
        return (Task.objects.filter(assignees=self.request.user).
                select_related("task_type").
                order_by("is_completed", "deadline"))

