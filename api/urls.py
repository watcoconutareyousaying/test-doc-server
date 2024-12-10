from django.urls import path
from api.views import (
    ProjectListView,
    ProjectDetailView,
    TestPlanListView,
    TestPlanDetailView,
    TestCaseListView,
    TestCaseDetailView,
    TestCoverageListView,
    DefectReportListView,
    DefectReportDetailView,
    TestreportListView,
)

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name='project'),
    path("projects/<int:pk>/",
         ProjectDetailView.as_view(), name='project_detail'),
    path("testplans/", TestPlanListView.as_view(), name='testplans'),
    path("testplans/<int:pk>/", TestPlanDetailView.as_view(), name='testplan_detail'),
    path("testcases/", TestCaseListView.as_view(), name="testcases"),
    path("testcase/<int:pk>/", TestCaseDetailView.as_view(), name='testcase_detail'),
    path("testcoverages/", TestCoverageListView.as_view(), name='testcoverages'),
    path("defect-report/", DefectReportListView.as_view(), name="defect_report"),
    path("defect-report/<int:pk>/", DefectReportDetailView.as_view(),
         name='defect_report_detail'),
    path("test-reports/", TestreportListView.as_view(), name="test_reports"),

    path("<int:pk>/testcases/", TestCaseListView.as_view(), name="export_testcases"),
    path("<int:pk>/defect-report/", DefectReportListView.as_view(), name="export_defect_report"),
    path("<int:pk>/test-reports/", TestreportListView.as_view(), name="export_test_reports"),
]
