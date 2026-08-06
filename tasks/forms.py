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


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
    )
    description = forms.CharField(
        required=False,
    )
    priorities = forms.MultipleChoiceField(
        required=False,
        choices=Task.Priority.choices,
        widget=forms.CheckboxSelectMultiple,
    )
    statuses = forms.MultipleChoiceField(
        required=False,
        choices=[
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )
    task_types = forms.ModelMultipleChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
