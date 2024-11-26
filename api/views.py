from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.models import Project, TestPlan, TestCase, TestCoverage, BugReport, TestReport
from api.serializers import (
    ProjectSerializer,
    TestPlanSerializer,
    TestCaseSerializer,
    TestCoverageSerializer,
    BugReportSerializer,
    TestReportSerializer,
)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def project_list(request):

    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def project_detail(request, pk):

    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testplan_list(request):

    if request.method == "GET":
        testplans = TestPlan.objects.all()
        serializer = TestPlanSerializer(testplans, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TestPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def testplan_detail(request, pk):
    try:
        testplan = TestPlan.objects.get(pk=pk)
    except TestPlan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TestPlanSerializer(testplan)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TestPlanSerializer(testplan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        testplan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testcase_list(request):

    if request.method == "GET":
        testcase = TestCase.objects.all()
        serializer = TestCaseSerializer(testcase, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TestCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def testcase_detail(request, pk):
    try:
        testcase = TestCase.objects.get(pk=pk)
    except TestCase.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TestCaseSerializer(testcase)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TestCaseSerializer(testcase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        testcase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testcoverage_list(request):

    if request.method == "GET":
        testcover = TestCoverage.objects.all()
        serializer = TestCoverageSerializer(testcover, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TestCoverageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def bugreport_list(request):

    if request.method == "GET":
        bugreport = BugReport.objects.all()
        serializer = BugReportSerializer(bugreport, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = BugReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testreport_list(request):

    if request.method == "GET":
        testreports = TestReport.objects.all()
        serializer = TestReportSerializer(testreports, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TestReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
