from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction


from api.models import Project, TestPlan, TestCase, TestCoverage, DefectReport, TestReport, TestCaseStatusHistory


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "created_by", "created_at", "updated_at")
        read_only_fields = ["created_by", "created_at", "updated_at"]


class TestPlanSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    class Meta:
        model = TestPlan
        fields = (
            "id",
            "name",
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
        read_only_fields = ["created_at", "updated_at"]


class TestCaseSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    class Meta:
        model = TestCase
        fields = (
            "id",
            "name",
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
        project = validated_data.get("project")

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Get the last TestCase for the same project
            last_testcase = TestCase.objects.filter(
                project=project).order_by("-id").first()
            last_id = int(last_testcase.testcaseID.split("_")
                          [1]) if last_testcase else 0
            next_id = last_id + 1
            new_testcaseID = f"TC_{next_id:04d}"

            # Ensure uniqueness of testcaseID
            while TestCase.objects.filter(testcaseID=new_testcaseID).exists():
                next_id += 1
                new_testcaseID = f"TC_{next_id:04d}"

            validated_data["testcaseID"] = validated_data.get(
                "testcaseID", new_testcaseID)

        # Create the TestCase object
        return TestCase.objects.create(**validated_data)


class TestCaseIDSerializer(serializers.Serializer):
    testcaseID = serializers.CharField(max_length=50)


class TestCoverageSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    test_cases = TestCaseIDSerializer(many=True)

    class Meta:
        model = TestCoverage
        fields = (
            "id",
            "name",
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

    def update_status(self, test_cases):
        all_pass = all(test_case.status ==
                       TestCase.StatusChoices.PASS for test_case in test_cases)
        if all_pass:
            return TestCoverage.StatusChoices.COVERED
        return TestCoverage.StatusChoices.NOT_COVERED

    def create(self, validated_data):
        project = validated_data["project"]
        test_cases_data = validated_data.pop('test_cases')

        test_coverage = TestCoverage.objects.create(**validated_data)

        for testcase_data in test_cases_data:
            testcase_instance = TestCase.objects.get(
                project=project,
                testcaseID=testcase_data['testcaseID']
            )
            test_coverage.test_cases.add(testcase_instance)

        new_status = self.update_status(
            test_coverage.test_cases.all())
        test_coverage.status = new_status
        test_coverage.save()

        return test_coverage


class DefectReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    evidence = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = DefectReport
        fields = (
            "title",
            "project",
            "defect_id",
            "summary",
            "steps_to_reproduce",
            "severity",
            "status",
            'evidence',
            'defect_detected_date',
            'defect_fixed_date',
            'reopen_defect_date',
            "created_at",
            "updated_at",
        )
        read_only_fields = ["defect_id", "created_at", "updated_at",
                            "defect_detected_date", "defect_fixed_date", "reopen_defect_date"]

        def validate_status(self, value):
            defect_report = getattr(self, 'instance', None)

            if defect_report:
                if value == DefectReport.StatusChoices.FIXED and not defect_report.defect_fixed_date:
                    raise serializers.ValidationError(
                        "defect_fixed_date must be set when status is 'Fixed'")

                if value == DefectReport.StatusChoices.OPEN and defect_report.defect_fixed_date and not defect_report.reopen_defect_date:
                    raise serializers.ValidationError(
                        "reopen_defect_date must be set when reopening a defect")

            return value


class TestReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    total_test_cases = serializers.IntegerField(read_only=True)
    passed_test_cases = serializers.IntegerField(read_only=True)
    failed_test_cases = serializers.IntegerField(read_only=True)
    defect_summary = serializers.JSONField(read_only=True)
    observations = serializers.CharField(read_only=True)
    recommendations = serializers.CharField(read_only=True)

    class Meta:
        model = TestReport
        fields = (
            "id",
            "name",
            "project",
            "total_test_cases",
            "passed_test_cases",
            "failed_test_cases",
            "defect_summary",
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

        defects = DefectReport.objects.filter(project=project)
        defect_summary = {
            severity: defects.filter(severity=severity).count()
            for severity in DefectReport.SeverityChoices.values
        }

        observations = (
            f"Out of {total_test_cases} test cases, {
                passed_test_cases} passed and "
            f"{failed_test_cases} failed. Found {len(defects)} defects."
        )
        recommendations = "Fix all critical issues before proceeding with the release."

        validated_data.update(
            {
                "total_test_cases": total_test_cases,
                "passed_test_cases": passed_test_cases,
                "failed_test_cases": failed_test_cases,
                "defect_summary": defect_summary,
                "observations": observations,
                "recommendations": recommendations,
            }
        )
        return super().create(validated_data)


class TestCaseStatusHistorySerializer(serializers.ModelSerializer):
    testcase = serializers.PrimaryKeyRelatedField(
        queryset=TestCase.objects.all())

    class Meta:
        model = TestCaseStatusHistory
        fields = ("testcase", "status", "recorded_at")
