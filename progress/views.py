from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone

from .models import Topic, Problem, ProgressEntry


class TrackerLoginView(LoginView):
    template_name = "progress/login.html"


@login_required
def dashboard(request):
    """
    Main view: shows every topic with its problems, and this user's progress
    against each one. Supports filtering by status and difficulty via query params.
    """
    status_filter = request.GET.get("status", "")
    difficulty_filter = request.GET.get("difficulty", "")

    topics = Topic.objects.prefetch_related("problems").all()

    # Build a lookup of {problem_id: ProgressEntry} for this user in one query
    # instead of hitting the DB per-problem in the template.
    progress_map = {
        pe.problem_id: pe
        for pe in ProgressEntry.objects.filter(user=request.user).select_related("problem")
    }

    topic_data = []
    for topic in topics:
        problems = topic.problems.all()
        if difficulty_filter:
            problems = problems.filter(difficulty=difficulty_filter)

        rows = []
        for problem in problems:
            entry = progress_map.get(problem.id)
            entry_status = entry.status if entry else "NOT_STARTED"
            if status_filter and entry_status != status_filter:
                continue
            rows.append({"problem": problem, "entry": entry, "status": entry_status})

        if rows:
            topic_data.append({"topic": topic, "rows": rows})

    total_problems = Problem.objects.count()
    solved_count = ProgressEntry.objects.filter(user=request.user, status="SOLVED").count()
    progress_pct = round((solved_count / total_problems) * 100) if total_problems else 0

    today = timezone.now().date()
    due_for_revision = (
        ProgressEntry.objects.filter(user=request.user, next_revision_date__lte=today)
        .select_related("problem")
        .order_by("next_revision_date")
    )

    context = {
        "topic_data": topic_data,
        "total_problems": total_problems,
        "solved_count": solved_count,
        "progress_pct": progress_pct,
        "due_for_revision": due_for_revision,
        "status_filter": status_filter,
        "difficulty_filter": difficulty_filter,
        "status_choices": ProgressEntry.STATUS_CHOICES,
        "difficulty_choices": Problem.DIFFICULTY_CHOICES,
    }
    return render(request, "progress/dashboard.html", context)


@login_required
def mark_status(request, problem_id, new_status):
    """Update a problem's status for the current user."""
    problem = get_object_or_404(Problem, id=problem_id)
    entry, _created = ProgressEntry.objects.get_or_create(user=request.user, problem=problem)

    if new_status == "SOLVED":
        entry.mark_solved()
        messages.success(request, f"Marked '{problem.name}' as solved. Revise on {entry.next_revision_date}.")
    else:
        entry.status = new_status
        entry.save()
        messages.info(request, f"Updated '{problem.name}' to {entry.get_status_display()}.")

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def update_notes(request, problem_id):
    """Save free-text notes for a problem (approach, mistakes, etc.)."""
    problem = get_object_or_404(Problem, id=problem_id)
    entry, _created = ProgressEntry.objects.get_or_create(user=request.user, problem=problem)

    if request.method == "POST":
        entry.notes = request.POST.get("notes", "")
        entry.save()
        messages.success(request, f"Notes saved for '{problem.name}'.")

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))
