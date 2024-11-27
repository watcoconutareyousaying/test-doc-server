from django import forms
from django.contrib import admin
from django.forms import ValidationError
from django.utils.timezone import localtime

from api.models import Project, TestPlan, TestCase, TestCoverage, BugReport, TestReport


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_by",
        "formatted_created_at",
        "formatted_updated_at",
    )

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"


@admin.register(TestPlan)
class TestPlanAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "formatted_created_at",
        "formatted_updated_at"
    )

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = (
        "testcaseID",
        "project",
        "status",
        "formatted_created_at",
        "formatted_updated_at",
    )
    readonly_fields = ("testcaseID",)

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"


@admin.register(TestCoverage)
class TestCoverageAdmin(admin.ModelAdmin):
    list_display = (
        "feature_id",
        "project",
        "status",
        "formatted_created_at",
        "formatted_updated_at",
    )
    readonly_fields = ("feature_id",)

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = (
        "bug_id",
        "project",
        "status",
        "severity",
        "evidence",
        "formatted_created_at",
        "formatted_updated_at",
    )
    readonly_fields = ("bug_id",)

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"


@admin.register(TestReport)
class TestReportAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "total_test_cases",
        "passed_test_cases",
        "failed_test_cases",
        "formatted_created_at",
        "formatted_updated_at",
    )

    def formatted_created_at(self, obj):
        return self.format_datetime(obj.created_at)

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        return self.format_datetime(obj.updated_at)

    formatted_updated_at.short_description = "Updated At"

    @staticmethod
    def format_datetime(value):
        """Formats a datetime object to the required format."""
        if value:
            return localtime(value).strftime("%Y-%m-%d %H:%M:%S")
        return "-"
