from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.TrackerLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("problem/<int:problem_id>/mark/<str:new_status>/", views.mark_status, name="mark_status"),
    path("problem/<int:problem_id>/notes/", views.update_notes, name="update_notes"),
]
