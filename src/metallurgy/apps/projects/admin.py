from django.contrib import admin
from .models import Project, WorkDay


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    pass
