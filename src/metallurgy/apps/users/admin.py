from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee, Customer

# Register your models here.
UserAdmin.fieldsets[1][1]['fields'] = (
    'first_name', 'last_name', 'email', 'bio'
)

admin.site.register(User, UserAdmin)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
