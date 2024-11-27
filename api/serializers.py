from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from api.models import Project, TestPlan, TestCase, TestCoverage, BugReport, TestReport


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "created_by")
        read_only_fields = ["created_by"]


class TestPlanSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    class Meta:
        model = TestPlan
        fields = (
            "id",
            "project",
            "objective",
            "scope_in",
            "scope_out",
            "test_levels",
            "types_of_testing",
            "environment_details",
            "test_data",
            "test_manager",
            "test_leads",
            "testers",
            "developers",
            "business_analysts",
            "milestones",
            "deadlines",
            "dependencies",
            "deliverables",
            "entry_criteria",
            "exit_criteria",
            "risks",
            "mitigation_strategies",
            "defect_management",
            "communication_plan",
            "approval_process",
            "sign_off_authorities",
            "created_at",
            "updated_at",
        )


class TestCaseSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    class Meta:
        model = TestCase
        fields = (
            "id",
            "project",
            "testcaseID",
            "description",
            "preconditions",
            "test_steps",
            "expected_result",
            "actual_result",
            "status",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"testcaseID": {"required": False}}

    def create(self, validated_data):
        return TestCase.objects.create(**validated_data)


class TestCoverageSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    test_cases = serializers.SerializerMethodField()
    # test_cases = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = TestCoverage
        fields = (
            "id",
            "project",
            "feature_id",
            "feature_description",
            "test_cases",
            "status",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "feature_id": {"required": False},
            "status": {"required": False},
        }

    def get_test_cases(self, obj):
        test_cases = obj.test_cases.all()
        return [test_case.testcaseID for test_case in test_cases]

    def create(self, validated_data):
        print("validated_data", validated_data)
        test_case_ids = validated_data.pop('test_cases', [])

        test_cases = TestCase.objects.filter(testcaseID__in=test_case_ids)

        # Create the TestCoverage object
        test_coverage = TestCoverage.objects.create(**validated_data)

        # Associate the TestCase instances with the TestCoverage object
        test_coverage.test_cases.set(test_cases)
        test_coverage.save()

        return test_coverage


class BugReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    evidence = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = BugReport
        fields = (
            "project",
            "bug_id",
            "summary",
            "steps_to_reproduce",
            "severity",
            "status",
            'evidence',
            "created_at",
            "updated_at",
        )
        read_only_fields = ["bug_id", "created_at", "updated_at"]


class TestReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    total_test_cases = serializers.IntegerField(read_only=True)
    passed_test_cases = serializers.IntegerField(read_only=True)
    failed_test_cases = serializers.IntegerField(read_only=True)
    bugs_summary = serializers.JSONField(read_only=True)
    observations = serializers.CharField(read_only=True)
    recommendations = serializers.CharField(read_only=True)

    class Meta:
        model = TestReport
        fields = (
            "id",
            "project",
            "total_test_cases",
            "passed_test_cases",
            "failed_test_cases",
            "bugs_summary",
            "observations",
            "recommendations",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        project = validated_data["project"]

        test_cases = TestCase.objects.filter(project=project)
        total_test_cases = test_cases.count()
        passed_test_cases = test_cases.filter(
            status=TestCase.StatusChoices.PASS
        ).count()
        failed_test_cases = test_cases.filter(
            status=TestCase.StatusChoices.FAIL
        ).count()

        bugs = BugReport.objects.filter(project=project)
        bugs_summary = {
            severity: bugs.filter(severity=severity).count()
            for severity in BugReport.SeverityChoices.values
        }

        observations = (
            f"Out of {total_test_cases} test cases, {
                passed_test_cases} passed and "
            f"{failed_test_cases} failed. Found {len(bugs)} bugs."
        )
        recommendations = "Fix all critical issues before proceeding with the release."

        validated_data.update(
            {
                "total_test_cases": total_test_cases,
                "passed_test_cases": passed_test_cases,
                "failed_test_cases": failed_test_cases,
                "bugs_summary": bugs_summary,
                "observations": observations,
                "recommendations": recommendations,
            }
        )
        return super().create(validated_data)
