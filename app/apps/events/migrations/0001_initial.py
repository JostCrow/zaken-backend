# Generated by Django 3.2.7 on 2021-11-16 09:57

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # ("cases", "0002_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = []
    # operations = [
    #     migrations.CreateModel(
    #         name="CaseEvent",
    #         fields=[
    #             (
    #                 "id",
    #                 models.AutoField(
    #                     auto_created=True,
    #                     primary_key=True,
    #                     serialize=False,
    #                     verbose_name="ID",
    #                 ),
    #             ),
    #             ("date_created", models.DateTimeField(auto_now_add=True)),
    #             (
    #                 "type",
    #                 models.CharField(
    #                     choices=[
    #                         ("DEBRIEFING", "DEBRIEFING"),
    #                         ("VISIT", "VISIT"),
    #                         ("CASE", "CASE"),
    #                         ("CASE_CLOSE", "CASE_CLOSE"),
    #                         ("SUMMON", "SUMMON"),
    #                         ("GENERIC_TASK", "GENERIC_TASK"),
    #                         ("SCHEDULE", "SCHEDULE"),
    #                         ("CITIZEN_REPORT", "CITIZEN_REPORT"),
    #                     ],
    #                     max_length=250,
    #                 ),
    #             ),
    #             ("emitter_id", models.PositiveIntegerField()),
    #             (
    #                 "case",
    #                 models.ForeignKey(
    #                     on_delete=django.db.models.deletion.CASCADE,
    #                     related_name="events",
    #                     to="cases.case",
    #                 ),
    #             ),
    #             (
    #                 "emitter_type",
    #                 models.ForeignKey(
    #                     on_delete=django.db.models.deletion.CASCADE,
    #                     to="contenttypes.contenttype",
    #                 ),
    #             ),
    #         ],
    #         options={
    #             "ordering": ["date_created"],
    #         },
    #     ),
    # ]
