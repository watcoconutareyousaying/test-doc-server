# Generated by Django 5.1.3 on 2024-11-27 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_bugreport_evidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='testcaseID',
            field=models.CharField(max_length=10),
        ),
    ]
