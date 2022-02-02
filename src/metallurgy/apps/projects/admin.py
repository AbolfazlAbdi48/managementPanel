from django.contrib import admin
from .models import Project, WorkDay, Factor, FactorDetail


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    pass


class FactorDetailInline(admin.TabularInline):
    model = FactorDetail


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    inlines = [
        FactorDetailInline
    ]


@admin.register(FactorDetail)
class FactorDetailAdmin(admin.ModelAdmin):
    pass
