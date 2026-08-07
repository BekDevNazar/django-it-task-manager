from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from tasks.forms import TaskTypeForm, PositionForm
from tasks.models import TaskType, Position


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_types/task_type_list.html"
    context_object_name = "task_types"
    paginate_by = 5

    def get_queryset(self):
        return TaskType.objects.annotate(
            task_count=Count("tasks")).order_by("name")


class TaskTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_types/task_type_form.html"
    context_object_name = "task_type"

    permission_required = "tasks.add_tasktype"
    raise_exception = True


class TaskTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "task_types/task_type_form.html"
    context_object_name = "task_type"

    permission_required = "tasks.change_tasktype"
    raise_exception = True


class TaskTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_types/task_type_confirm_delete.html"
    success_url = reverse_lazy("references:task-type-list")

    permission_required = "tasks.delete_tasktype"
    raise_exception = True


    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "You cannot delete this task type because it is used by existing tasks.",
            )
            return redirect("references:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "positions/position_list.html"
    context_object_name = "positions"
    paginate_by = 5

    def get_queryset(self):
        return (
            Position.objects.annotate(worker_count=Count("workers")).order_by("name")
        )


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    template_name = "positions/position_form.html"
    context_object_name = "position"

    permission_required = "tasks.add_position"
    raise_exception = True


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "positions/position_form.html"
    context_object_name = "position"

    permission_required = "tasks.change_position"
    raise_exception = True


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "positions/position_confirm_delete.html"
    success_url = reverse_lazy("references:position-list")

    permission_required = "tasks.delete_position"
    raise_exception = True
