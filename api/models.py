from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Project(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name


class TestPlan(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
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
        db_table = 'testplan'

    def __str__(self) -> str:
        return self.project_id.name
