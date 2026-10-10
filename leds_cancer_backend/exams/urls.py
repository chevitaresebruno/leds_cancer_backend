from typing import Any

from django.urls import path, re_path

from .views import (
    DashboardStatsView,
    ExamDetailView,
    ExamDownloadView,
    ExamImageDownloadView,
    ExamImageTokenView,
    ExamListCreateView,
    RecentExamsView,
)

urlpatterns: list[Any] = [
    # Dashboard
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    # Exams
    path("exams/", ExamListCreateView.as_view(), name="exam-list-create"),
    path("exams/recent/", RecentExamsView.as_view(), name="exam-recent"),
    path("exams/<int:pk>/", ExamDetailView.as_view(), name="exam-detail"),
    # Image access
    path(
        "exams/image-token/<int:pk>/",
        ExamImageTokenView.as_view(),
        name="exam-image-token",
    ),
    re_path(
        r"^exams/image/(?P<pk>\d+)/?$",  # exams/image/<int:pk> and exams/image/<int:pk>/ are both valid
        ExamImageDownloadView.as_view(),
        name="exam-image-download",
    ),
    path(
        "exams/<int:pk>/download/",
        ExamDownloadView.as_view(),
        name="exam-report-download",
    ),
]
