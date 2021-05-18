# Generated by Django 3.1.8 on 2021-05-17 15:02

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cases", "0052_delete_citizenreport"),
    ]

    operations = [
        migrations.CreateModel(
            name="CitizenReport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "camunda_task_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "reporter_name",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "reporter_phone",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("identification", models.PositiveIntegerField()),
                (
                    "advertisement_linklist",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        default=list,
                        null=True,
                        size=None,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="case_citizen_reports",
                        to="cases.case",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
