# Generated by Django 5.1.3 on 2024-11-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_testcase_testcaseid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='bug_id',
            field=models.CharField(max_length=10),
        ),
    ]