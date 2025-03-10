import os
import datetime
from django.utils.timezone import now
from django.db import models, transaction
# from django.contrib.auth.models import AbstractUser
from account.models import UserData


# class User(AbstractUser):
#     pass


class Project(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project"

    def __str__(self):
        return self.name


class TestPlan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    objective = models.TextField()
    scope_in = models.TextField()
    scope_out = models.TextField()
    test_levels = models.CharField(max_length=255)
    types_of_testing = models.CharField(max_length=255)
    environment_details = models.TextField()
    test_data = models.TextField()
    test_manager = models.CharField(max_length=255)
    test_leads = models.CharField(max_length=255)
    testers = models.TextField()
    developers = models.TextField()
    business_analysts = models.TextField()
    milestones = models.TextField()
    deadlines = models.TextField()
    dependencies = models.TextField()
    deliverables = models.TextField()
    entry_criteria = models.TextField()
    exit_criteria = models.TextField()
    risks = models.TextField()
    mitigation_strategies = models.TextField()
    defect_management = models.TextField()
    communication_plan = models.TextField()
    approval_process = models.TextField()
    sign_off_authorities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "testplan"

    def __str__(self) -> str:
        return self.project.name


class TestCase(models.Model):

    class StatusChoices(models.TextChoices):
        PASS = "Pass"
        FAIL = "Fail"
        PENDING = "Pending"

    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="test_cases"
    )
    testcaseID = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    preconditions = models.TextField(blank=True)
    test_steps = models.TextField()
    expected_result = models.TextField()
    actual_result = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "testcase"

    def save(self, *args, **kwargs):
        if not self.testcaseID:
            with transaction.atomic():
                last_testcase = TestCase.objects.filter(
                    project=self.project).order_by("-id").first()
                last_id = (
                    int(last_testcase.testcaseID.split(
                        "_")[1]) if last_testcase else 0
                )
                next_id = last_id + 1
                new_testcaseID = f"TC_{next_id:04d}"

                # Ensure uniqueness of testcaseID
                while TestCase.objects.filter(testcaseID=new_testcaseID).exists():
                    next_id += 1
                    new_testcaseID = f"TC_{next_id:04d}"

                self.testcaseID = new_testcaseID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.testcaseID} - {self.project.name}"


class TestCoverage(models.Model):
    class StatusChoices(models.TextChoices):
        COVERED = "Covered"
        NOT_COVERED = "Not Covered"

    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    feature_id = models.CharField(max_length=20, unique=True)
    feature_description = models.TextField()
    test_cases = models.ManyToManyField(
        TestCase, related_name="test_coverages")
    status = models.CharField(
        max_length=20, choices=StatusChoices, default=StatusChoices.NOT_COVERED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "testcoverage"

    def __str__(self):
        return f"Feature {self.feature_id} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.feature_id:
            with transaction.atomic():
                last_feature = TestCoverage.objects.filter(
                    project=self.project).order_by("-feature_id").first()

                if last_feature and last_feature.feature_id.startswith("FTR_"):
                    last_id = int(last_feature.feature_id.split("_")[1])
                    new_id = f"FTR_{last_id + 1:04d}"
                else:
                    last_id = 0
                    new_id = "FTR_0001"

                while TestCoverage.objects.filter(feature_id=new_id).exists():
                    last_id += 1
                    new_id = f"FTR_{last_id + 1:04d}"

                self.feature_id = new_id
        super().save(*args, **kwargs)


class DefectReport(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = "Open"
        CLOSED = "Closed"
        INPROGRESS = "In Progress"
        FIXED = "Fixed"

    class SeverityChoices(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"
        CRITICAL = "Critical"

    title = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    defect_id = models.CharField(max_length=30, unique=True)
    summary = models.TextField()
    steps_to_reproduce = models.TextField()
    severity = models.CharField(max_length=10, choices=SeverityChoices)
    status = models.CharField(
        max_length=15, choices=StatusChoices, default=StatusChoices.OPEN
    )
    evidence = models.FileField(
        upload_to='defect_reports/evidence/', null=True, blank=True)
    defect_detected_date = models.DateTimeField(null=True, blank=True)
    defect_fixed_date = models.DateTimeField(null=True, blank=True)
    reopen_defect_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.defect_id:
            last_defect = DefectReport.objects.filter(
                project=self.project).order_by("-id").first()

            if last_defect:
                if last_defect.defect_id.startswith("DEFECT_"):
                    last_id = int(last_defect.defect_id[7:])
                    new_id = f"DEFECT_{last_id + 1:04d}"
                else:
                    new_id = "DEFECT_0001"
            else:
                last_id = 0
                new_id = "DEFECT_0001"

            while DefectReport.objects.filter(defect_id=new_id).exists():
                last_id += 1
                new_id = f"DEFECT_{last_id + 1:04d}"

            self.defect_id = new_id

            if self.status == self.StatusChoices.OPEN and not self.defect_detected_date:
                self.defect_detected_date = datetime.datetime.now()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.evidence:
            if os.path.isfile(self.evidence.path):
                os.remove(self.evidence.path)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = "defect_report"

    def __str__(self):
        return f"{self.defect_id} - {self.project.name}"


class TestReport(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="test_reports"
    )
    total_test_cases = models.IntegerField()
    passed_test_cases = models.IntegerField()
    failed_test_cases = models.IntegerField()
    defect_summary = models.JSONField()
    observations = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "testreport"

    def __str__(self):
        return f"Test Report for Project {self.project.name}"


class TestCaseStatusHistory(models.Model):
    testcase = models.ForeignKey(
        TestCase, on_delete=models.CASCADE, related_name="status_history"
    )
    status = models.CharField(
        max_length=10, choices=TestCase.StatusChoices.choices)
    recorded_at = models.DateField(default=now)

    class Meta:
        db_table = "testcase_status"
        unique_together = ("testcase", "recorded_at")

    def __str__(self):
        return f"{self.testcase.testcaseID}: {self.status} on {self.recorded_at}"
