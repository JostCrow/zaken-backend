# Generated by Django 3.2.5 on 2021-09-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workflow", "0018_remove_workflow_workflow_spec"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
