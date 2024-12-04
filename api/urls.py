from django.urls import path
from api.views import (
    ProjectListView,
    ProjectDetailView,
    TestPlanListView,
    TestPlanDetailView,
    TestCaseListView,
    TestCaseDetailView,
    TestCoverageListView,
    BugreportListView,
    TestreportListView,
)

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name='project'),
    path("projects/<int:pk>/",
         ProjectDetailView.as_view(), name='project-detail'),
    path("testplans/", TestPlanListView.as_view(), name='testplans'),
    path("testplans/<int:pk>/", TestPlanDetailView.as_view(), name='testplan-detail'),
    path("testcases/", TestCaseListView.as_view(), name="testcases"),
    path("testcase/<int:pk>/", TestCaseDetailView.as_view(), name='testcase-detail'),
    path("testcoverages/", TestCoverageListView.as_view(), name='testcoverages'),
    path("bugreport/", BugreportListView.as_view(), name="bug_report"),
    path("testreport/", TestreportListView.as_view(), name="test_report"),
]
