# Generated by Django 5.1.3 on 2025-02-21 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_testcasestatushistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='defectreport',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='testcase',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='testcoverage',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='testplan',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='testreport',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
