from django.contrib import admin
from .models import Topic, Problem, ProgressEntry


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("week_number", "title")
    ordering = ("week_number",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "difficulty", "pattern")
    list_filter = ("topic", "difficulty")
    search_fields = ("name", "pattern")


@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "problem", "status", "date_solved", "next_revision_date")
    list_filter = ("status", "problem__topic")
    search_fields = ("problem__name", "user__username")
