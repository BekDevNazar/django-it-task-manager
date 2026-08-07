from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Task, Worker, Position, TaskType

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Additional information",{"fields": ("position",),},),)

    add_fieldsets = UserAdmin.add_fieldsets + (("Additional information",{"fields": ("position",),},),)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "position",
        "is_staff",
    )

admin.site.register(Position)
admin.site.register(TaskType)

