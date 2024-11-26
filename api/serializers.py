from rest_framework import serializers

from api.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'created_by'
        )
        read_only_fields = ['created_by']


class TestPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPlan
        fields = (
            'id',
            'project_id',
            'objective',
            'scope_in',
            'scope_out',
            'test_levels',
            'types_of_testing',
            'environment_details',
            'test_data',
            'test_manager',
            'test_leads',
            'testers',
            'developers',
            'business_analysts',
            'milestones',
            'deadlines',
            'dependencies',
            'deliverables',
            'entry_criteria',
            'exit_criteria',
            'risks',
            'mitigation_strategies',
            'defect_management',
            'communication_plan',
            'approval_process',
            'sign_off_authorities',
        )
