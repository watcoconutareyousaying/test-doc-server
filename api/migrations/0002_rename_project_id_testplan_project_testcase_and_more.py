# Generated by Django 5.1.3 on 2024-11-26 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testplan',
            old_name='project_id',
            new_name='project',
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcaseID', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField()),
                ('preconditions', models.TextField(blank=True)),
                ('test_steps', models.TextField()),
                ('expected_result', models.TextField()),
                ('actual_result', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='api.project')),
            ],
            options={
                'db_table': 'testcase',
            },
        ),
        migrations.CreateModel(
            name='TestCoverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.CharField(max_length=20, unique=True)),
                ('feature_description', models.TextField()),
                ('status', models.CharField(choices=[('Covered', 'Covered'), ('Not Covered', 'Not Covered')], default='Not Covered', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project')),
                ('test_cases', models.ManyToManyField(related_name='test_coverages', to='api.testcase')),
            ],
            options={
                'db_table': 'testcoverage',
            },
        ),
    ]
