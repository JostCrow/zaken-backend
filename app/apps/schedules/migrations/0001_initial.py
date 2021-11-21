# Generated by Django 3.2.7 on 2021-11-16 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cases", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("name", models.CharField(max_length=255)),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="cases.casetheme",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("name", "theme")},
            },
        ),
        migrations.CreateModel(
            name="DaySegment",
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
                ("name", models.CharField(max_length=255)),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="day_segments",
                        to="cases.casetheme",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("name", "theme")},
            },
        ),
        migrations.CreateModel(
            name="Priority",
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
                ("name", models.CharField(max_length=255)),
                ("weight", models.FloatField()),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="priorities",
                        to="cases.casetheme",
                    ),
                ),
            ],
            options={
                "ordering": ["weight"],
                "unique_together": {("name", "theme")},
            },
        ),
        migrations.CreateModel(
            name="WeekSegment",
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
                ("name", models.CharField(max_length=255)),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="week_segments",
                        to="cases.casetheme",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("name", "theme")},
            },
        ),
        migrations.CreateModel(
            name="Schedule",
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
                ("case_user_task_id", models.CharField(default="-1", max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedules.action",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="cases.case",
                    ),
                ),
                (
                    "day_segment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedules.daysegment",
                    ),
                ),
                (
                    "priority",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedules.priority",
                    ),
                ),
                (
                    "week_segment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedules.weeksegment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
