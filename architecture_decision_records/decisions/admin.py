"""Django admin customization."""
from django.contrib import admin

from . import models


# @admin.register(models.Decision)
# class DecisionAdmin(admin.ModelAdmin):
#     """Define the admin pages for Decisions."""

#     ordering = ["-id"]
#     list_display = ("slug", "title", "status", "user")


# @admin.register(models.RevisionComment)
# class RevisionCommentAdmin(admin.ModelAdmin):
#     """Define the admin pages for Decisions."""

#     ordering = ["-id"]
#     list_display = ("content", "date_created", "user", "version")


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """Define the admin pages for Status."""

    pass
