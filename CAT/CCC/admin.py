from django.contrib import admin
from CCC.models import Job, Module

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 3

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('job', 'name', 'tag', 'hash_value')

class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Job Information', {'fields': ['branch', 'build_start_time', 'assignee']}),
    ]
    inlines = [ModuleInline]
    list_display = ('branch', 'build_start_time', 'assignee')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(Module, ModuleAdmin)

