import os
import openpyxl
from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from openpyxl.styles import PatternFill, Font
from typing import Dict, Optional, cast

from server import settings
from api.models import Project, TestPlan, TestCase, TestCoverage, BugReport, TestReport
from api.serializers import (
    ProjectSerializer,
    TestPlanSerializer,
    TestCaseSerializer,
    TestCoverageSerializer,
    BugReportSerializer,
    TestReportSerializer,
)

# handle project list
# Created by      :   Nantha
# Created date    :   26/11/2024


class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# handle project detail [retrieve-update-destory]
# Created by      :   Nantha
# Created date    :   26/11/2024


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# handle testplan [list/create]
# Created by      :   Nantha
# Created date    :   26/11/2024


class TestPlanListView(generics.ListCreateAPIView):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    permission_classes = [IsAuthenticated]

# handle Testplan detail [retrive-update-destory]
# Created by      :   Nantha
# Created date    :   26/11/2024
# Updated date    :   04/12/2024


class TestPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if 'export' in request.query_params:
            return self.export_file(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def export_file(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data: Dict[str, Optional[str]] = cast(
            Dict[str, Optional[str]], response.data)

        project_id: Optional[str] = data.get('project')
        project_name = Project.objects.filter(id=project_id).values_list(
            'name', flat=True).first() if project_id else None

        data['project'] = project_name or f"Unknown Project (ID: {project_id})"
        # return response
        print(data)

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        assert sheet is not None, "Failed"

        sheet.title = 'Test Plan'

        header_fill = PatternFill(
            start_color="22f071", end_color="22f071", fill_type="solid")
        header_font = Font(bold=True)

        headers = ["Sections", "Description"]

        sheet.append(headers)

        for cell in sheet[1]:
            cell.fill = header_fill
            cell.font = header_font

        sections = [
            ("Project", data.get('project')),
            ("Objective", data.get('objective')),
            ("Scope In", data.get('scope_in')),
            ("Scope Out", data.get('scope_out')),
            ("Test Levels", data.get('test_levels')),
            ("Types of Testing", data.get('types_of_testing')),
            ("Environment Details", data.get('environment_details')),
            ("Test Data", data.get('test_data')),
            ("Test Manager", data.get('test_manager')),
            ("Test Leads", data.get('test_leads')),
            ("Testers", data.get('testers')),
            ("Developers", data.get('developers')),
            ("Business Analysts", data.get('business_analysts')),
            ("Milestones", data.get('milestones')),
            ("Deadlines", data.get('deadlines')),
            ("Dependencies", data.get('dependencies')),
            ("Deliverables", data.get('deliverables')),
            ("Entry Criteria", data.get('entry_criteria')),
            ("Exit Criteria", data.get('exit_criteria')),
            ("Risks", data.get('risks')),
            ("Mitigation Strategies", data.get(
                'mitigation_strategies')),
            ("Defect Management", data.get('defect_management')),
            ("Communication Plan", data.get('communication_plan')),
            ("Approval Process", data.get('approval_process')),
            ("Sign-off Authorities", data.get('sign_off_authorities')),
        ]

        for section, description in sections:
            sheet.append([section, description])

        media_root = settings.MEDIA_ROOT
        download_path = os.path.join(media_root, 'download')
        os.makedirs(download_path, exist_ok=True)  # Ensure the folder exists

        file_path = os.path.join(download_path, 'testplan.xlsx')

        # Save the workbook to the file path
        workbook.save(file_path)

        # Respond with the file location or success message
        return Response({
            'message': 'File has been successfully saved.',
            'file_path': file_path,
        })

# handle Testcase [list/create]
# Created by      :   Nantha
# Created date    :   26/11/2024


class TestCaseListView(generics.ListCreateAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]

# handle Testcase detail [retrieve-update-destory]
# Created by      :   Nantha
# Created date    :   26/11/2024


class TestCaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated]


# handle Testcoverage [list/create]
# Created by      :   Nantha
# Created date    :   26/11/2024

class TestCoverageListView(generics.ListCreateAPIView):
    queryset = TestCoverage.objects.all()
    serializer_class = TestCoverageSerializer
    permission_classes = [IsAuthenticated]

# handle Bugreport [list/create]
# Created by      :   Nantha
# Created date    :   04/12/2024


class BugreportListView(generics.ListCreateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = [IsAuthenticated]

# handle Testreport [list/create]
# Created by      :   Nantha
# Created date    :   04/12/2024


class TestreportListView(generics.ListCreateAPIView):
    queryset = TestReport.objects.all()
    serializer_class = TestReportSerializer
    permission_classes = [IsAuthenticated]
