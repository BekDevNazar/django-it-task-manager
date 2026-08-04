from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from tasks.models import Task, Worker, Position, TaskType

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed"]


admin.site.register(Worker, UserAdmin)
admin.site.register(Position)
admin.site.register(TaskType)

admin.site.unregister(Group)
