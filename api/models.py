import os
from django.db import models
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

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="test_cases"
    )
    testcaseID = models.CharField(max_length=10)
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
            # last_testcase = TestCase.objects.order_by("-id").first()
            last_testcase = TestCase.objects.filter(
                project=self.project).order_by("-id").first()
            last_id = (
                int(last_testcase.testcaseID.split(
                    "_")[1]) if last_testcase else 0
            )
            next_id = last_id + 1
            self.testcaseID = f"TC_{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.testcaseID} - {self.project.name}"


class TestCoverage(models.Model):
    class StatusChoices(models.TextChoices):
        COVERED = "Covered"
        NOT_COVERED = "Not Covered"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    feature_id = models.CharField(max_length=20)
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
            last_feature = TestCoverage.objects.filter(
                project=self.project).order_by("-id").first()
            if last_feature:
                last_id = int(last_feature.feature_id.split("_")[1])
                new_id = f"FTR_{last_id + 1:04d}"
            else:
                new_id = "FTR_0001"
            self.feature_id = new_id
        super().save(*args, **kwargs)

    def update_status(self):
        if all(test_case.status == "Pass" for test_case in self.test_cases.all()):
            self.status = self.StatusChoices.COVERED
        else:
            self.status = self.StatusChoices.NOT_COVERED
        self.save()


class BugReport(models.Model):
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

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bug_id = models.CharField(max_length=10)
    summary = models.TextField()
    steps_to_reproduce = models.TextField()
    severity = models.CharField(max_length=10, choices=SeverityChoices)
    status = models.CharField(
        max_length=15, choices=StatusChoices, default=StatusChoices.OPEN
    )
    evidence = models.FileField(
        upload_to='bug_reports/evidence/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.bug_id:
            # last_bug = BugReport.objects.all().order_by("id").last()
            last_bug = BugReport.objects.filter(
                project=self.project).order_by("-id").first()
            if last_bug:
                last_id = int(last_bug.bug_id[3:])
                new_id = f"BUG{last_id + 1:04d}"
            else:
                new_id = "BUG0001"
            self.bug_id = new_id
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.evidence:
            if os.path.isfile(self.evidence.path):
                os.remove(self.evidence.path)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = "bugreport"

    def __str__(self):
        return f"{self.bug_id} - {self.project.name}"


class TestReport(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="test_reports"
    )
    total_test_cases = models.IntegerField()
    passed_test_cases = models.IntegerField()
    failed_test_cases = models.IntegerField()
    bugs_summary = models.JSONField()
    observations = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "testreport"

    def __str__(self):
        return f"Test Report for Project {self.project.name}"
