# Generated by Django 3.2.5 on 2021-09-08 08:07

import uuid

from django.db import migrations, models


def create_uuid(apps, schema_editor):
    Task = apps.get_model("workflow", "Task")
    for task in Task.objects.all():
        task.task_id = uuid.uuid4()
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0011_task_form"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="task_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name="task",
            name="task_id",
            field=models.UUIDField(
                unique=True,
            ),
        ),
    ]
