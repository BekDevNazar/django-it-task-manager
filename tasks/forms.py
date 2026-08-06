from django import forms

from tasks.models import Task, TaskType, Position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees",
        ]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
