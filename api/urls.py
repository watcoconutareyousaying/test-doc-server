from django.urls import path
from api.views import (
    project_list,
    project_detail,
    testplan_list,
    testplan_detail,
    testcase_list,
    testcase_detail,
    testcoverage_list,
    bugreport_list,
    testreport_list,
)

urlpatterns = [
    path("project/", project_list, name="project"),
    path("project-detail/<int:pk>/", project_detail, name="project_detail"),
    path("testplan/", testplan_list, name="test_plan"),
    path("testplan_detail/<int:pk>/", testplan_detail, name="testplan_detail"),
    path("testcase/", testcase_list, name="test_case"),
    path("testcase_detail/<int:pk>/", testcase_detail, name="testcase_detail"),
    path("testcoverage/", testcoverage_list, name="test_coverage"),
    path("bugreport/", bugreport_list, name="bug_report"),
    path("testreport/", testreport_list, name="test_report"),
]
