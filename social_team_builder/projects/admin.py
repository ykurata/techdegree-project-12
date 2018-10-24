from django.contrib import admin

from .models import Project, Position


class PositionInline(admin.StackedInline):
    model = Position


class ProjectAdmin(admin.ModelAdmin):
    inlines = [PositionInline,]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Position)
