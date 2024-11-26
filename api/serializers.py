from rest_framework import serializers

from api.models import Project, TestPlan, TestCase, TestCoverage, BugReport, TestReport


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "created_by")
        read_only_fields = ["created_by"]


class TestPlanSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

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
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

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
            # Ensure the `testcaseID` is generated when creating the instance
            testcase = TestCase(**validated_data)
            testcase.save()
            return testcase


class TestCoverageSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    test_cases = serializers.SerializerMethodField()

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

    def get_test_cases(self, obj):
        return [test_case.testcaseID for test_case in obj.test_cases.all()]

    def create(self, validated_data):
        test_cases_data = validated_data.pop("test_cases")
        test_coverage = TestCoverage.objects.create(**validated_data)
        for test_case_data in test_cases_data:
            test_case = TestCase.objects.get(testcaseID=test_case_data["testcaseID"])
            test_coverage.test_cases.add(test_case)
        test_coverage.update_status()  # Update the status based on the test cases
        return test_coverage

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop("test_cases", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update test cases
        if test_cases_data:
            instance.test_cases.clear()  # Clear the existing test cases
            for test_case_data in test_cases_data:
                test_case = TestCase.objects.get(
                    testcaseID=test_case_data["testcaseID"]
                )
                instance.test_cases.add(test_case)

        instance.update_status()  # Update status based on new test cases
        return instance


class BugReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = BugReport
        fields = (
            "project",
            "bug_id",
            "summary",
            "steps_to_reproduce",
            "severity",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["bug_id", "created_at", "updated_at"]


class TestReportSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    total_test_cases = serializers.IntegerField(read_only=True)
    passed_test_cases = serializers.IntegerField(read_only=True)
    failed_test_cases = serializers.IntegerField(read_only=True)
    bugs_summary = serializers.JSONField(read_only=True)
    observations = serializers.CharField(read_only=True)
    recommendations = serializers.CharField(read_only=True)

    class Meta:
        model = TestReport
        fields = (
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
            f"Out of {total_test_cases} test cases, {passed_test_cases} passed and "
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
