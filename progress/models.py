from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone


class Topic(models.Model):
    """Represents a week/theme in the roadmap, e.g. 'Week 1: Arrays & Hashing'."""
    week_number = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["week_number"]

    def __str__(self):
        return f"Week {self.week_number}: {self.title}"


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="problems")
    name = models.CharField(max_length=200)
    pattern = models.CharField(max_length=100, blank=True, help_text="e.g. Two Pointers, Sliding Window")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="MEDIUM")
    leetcode_url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["topic__week_number", "order"]

    def __str__(self):
        return self.name


class ProgressEntry(models.Model):
    """Tracks a specific user's progress on a specific problem."""
    STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("ATTEMPTED", "Attempted"),
        ("SOLVED", "Solved"),
        ("NEEDS_REVISION", "Needs Revision"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress_entries")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="progress_entries")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NOT_STARTED")
    date_solved = models.DateField(null=True, blank=True)
    next_revision_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "problem")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.username} - {self.problem.name} ({self.status})"

    def mark_solved(self):
        """Marks solved today and schedules spaced-revision using a simple interval ladder."""
        self.status = "SOLVED"
        self.attempts += 1
        today = timezone.now().date()
        self.date_solved = today
        # Spaced repetition ladder: 1st solve -> revise in 3 days, 2nd -> 7 days, 3rd+ -> 14 days
        interval_map = {1: 3, 2: 7}
        days = interval_map.get(self.attempts, 14)
        self.next_revision_date = today + timedelta(days=days)
        self.save()

    def get_absolute_url(self):
        return reverse("problem_detail", args=[self.problem.id])
